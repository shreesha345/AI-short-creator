import json
import logging
import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=dotenv_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize OpenAI client
try:
    # Validate API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY environment variable not set")
        client = None
    else:
        client = OpenAI(api_key=api_key)
        logging.info("OpenAI client initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize OpenAI client: {e}")
    client = None

# Define dynamic paths
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
INPUT_DIR = os.path.join(DATA_DIR, "input")
SUBTITLE_FILE_PATH = os.path.join(INPUT_DIR, "raw_video", "subtitles.srt")
OUTPUT_JSON_PATH = os.path.join(INPUT_DIR, "main_part.json")
MOCK_DATA_PATH = os.path.join(INPUT_DIR, "mock_main_part.json")


def read_subtitle_file(file_path):
    """Reads and returns the content of the subtitle file."""
    if not file_path or not isinstance(file_path, str):
        logging.error("Invalid file path provided")
        return None

    try:
        if not os.path.exists(file_path):
            logging.error(f"Subtitle file not found at: {file_path}")
            return None

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        if not content or not content.strip():
            logging.error("Subtitle file is empty")
            return None

        logging.info(f"Successfully read subtitle file: {len(content)} characters")
        return content

    except FileNotFoundError:
        logging.error(f"Subtitle file not found at: {file_path}")
        return None
    except UnicodeDecodeError as e:
        logging.error(f"Error decoding subtitle file: {e}")
        return None
    except Exception as e:
        logging.error(f"Error reading subtitle file: {e}")
        return None


def analyze_transcript(subtitle_content):
    """
    Analyzes the transcript content using OpenAI to find viral sections
    and saves the result to a JSON file.

    Args:
        subtitle_content (str): The subtitle content to analyze

    Returns:
        str: Path to the output JSON file if successful, None otherwise
    """
    if not client:
        logging.error("OpenAI client not initialized. Aborting analysis.")
        return None

    if not subtitle_content or not isinstance(subtitle_content, str):
        logging.error("No valid subtitle content provided. Aborting analysis.")
        return None

    if len(subtitle_content.strip()) < 50:
        logging.error("Subtitle content too short for analysis.")
        return None

    example_format = [
        {
            "start_time": 0.0,
            "end_time": 55.26,
            "description": "main description",
            "duration": 55.26,
        },
        {
            "start_time": 57.0,
            "end_time": 107.96,
            "description": "second main description",
            "duration": 50.96,
        },
    ]

    prompt = (
        f"This is a transcript of a video. Please identify the most viral sections from this transcript. "
        f"Each section must be more than 30 seconds in duration. Provide extremely accurate timestamps. "
        f"Respond ONLY in this JSON format: {json.dumps(example_format)}. "
        f"I just want a valid JSON array as the response, nothing else.\n\n"
        f"Here is the Transcription:\n{subtitle_content}"
    )

    messages: List[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": "You are ViralGPT, a helpful assistant skilled at identifying viral content in video transcripts between 30 and 58 seconds.",
        },
        {"role": "user", "content": prompt},
    ]

    model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-16k")

    try:
        logging.info(f"Sending request to OpenAI API with model: {model_name}...")

        # Validate model name
        if not model_name:
            model_name = "gpt-3.5-turbo-16k"
            logging.warning(f"No model specified, using default: {model_name}")

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            n=1,
            stop=None,
            response_format={"type": "json_object"},
            timeout=60,  # Add timeout
        )

        if not response or not response.choices:
            logging.error("No response received from OpenAI API")
            return None

        response_content = response.choices[0].message.content
        logging.info("Received response from OpenAI.")

        if not response_content:
            logging.error("Empty response content from OpenAI")
            return None

        # Validate JSON response
        try:
            viral_sections = json.loads(response_content)
        except json.JSONDecodeError as json_e:
            logging.error(f"Invalid JSON response from OpenAI: {json_e}")
            logging.debug(f"Response content: {response_content}")
            return None

        # Validate viral_sections structure
        if not isinstance(viral_sections, (list, dict)):
            logging.error("OpenAI response is not a valid list or dict")
            return None

        # If it's a dict, try to extract the array
        if isinstance(viral_sections, dict):
            # Look for common array keys
            for key in ["sections", "clips", "segments", "results"]:
                if key in viral_sections and isinstance(viral_sections[key], list):
                    viral_sections = viral_sections[key]
                    break
            else:
                logging.error("Could not find valid array in OpenAI response")
                return None

        # Validate each section has required fields
        valid_sections = []
        for i, section in enumerate(viral_sections):
            if not isinstance(section, dict):
                logging.warning(f"Section {i} is not a dictionary, skipping")
                continue

            required_fields = ["start_time", "end_time", "description"]
            if not all(field in section for field in required_fields):
                logging.warning(f"Section {i} missing required fields, skipping")
                continue

            try:
                start_time = float(section["start_time"])
                end_time = float(section["end_time"])
                duration = end_time - start_time

                if start_time < 0 or end_time <= start_time:
                    logging.warning(f"Section {i} has invalid timestamps, skipping")
                    continue

                if duration < 30:
                    logging.warning(
                        f"Section {i} duration {duration}s is too short, skipping"
                    )
                    continue

                # Update duration in section
                section["duration"] = duration
                valid_sections.append(section)

            except (ValueError, TypeError) as e:
                logging.warning(
                    f"Section {i} has invalid timestamp values: {e}, skipping"
                )
                continue

        if not valid_sections:
            logging.error("No valid sections found in OpenAI response")
            return None

        # Ensure output directory exists
        os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)

        # Write validated sections to file
        with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as json_file:
            json.dump(valid_sections, json_file, indent=2)

        logging.info(
            f"Successfully saved {len(valid_sections)} valid sections to {OUTPUT_JSON_PATH}"
        )
        return OUTPUT_JSON_PATH

    except json.JSONDecodeError as json_e:
        logging.error(f"JSON decode error: {json_e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred during OpenAI API call or file writing: {e}")
        return None


def main():
    """
    Main function to read subtitles, analyze them, and save the results.
    Supports a 'test mode' to bypass the OpenAI API.

    Returns:
        str: Path to output file if successful, None otherwise
    """
    logging.info("Starting transcript analysis...")

    # Ensure output directory exists
    try:
        os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create output directory: {e}")
        return None

    if os.getenv("TEST_MODE") == "true":
        logging.info("TEST_MODE is enabled. Using mock data.")
        try:
            if not os.path.exists(MOCK_DATA_PATH):
                logging.error(f"Mock data file not found at: {MOCK_DATA_PATH}")
                return None

            with open(MOCK_DATA_PATH, "r", encoding="utf-8") as mock_file:
                mock_data = json.load(mock_file)

            # Validate mock data structure
            if not isinstance(mock_data, list):
                logging.error("Mock data should be a list of segments")
                return None

            with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as output_file:
                json.dump(mock_data, output_file, indent=2)

            logging.info(
                f"Successfully wrote {len(mock_data)} mock segments to {OUTPUT_JSON_PATH}"
            )
            return OUTPUT_JSON_PATH

        except FileNotFoundError:
            logging.error(f"Mock data file not found at: {MOCK_DATA_PATH}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in mock data file: {e}")
            return None
        except Exception as e:
            logging.error(f"Error processing mock data: {e}")
            return None
    else:
        subtitle_content = read_subtitle_file(SUBTITLE_FILE_PATH)
        if subtitle_content:
            result = analyze_transcript(subtitle_content)
            if result:
                logging.info("Transcript analysis completed successfully")
                return result
            else:
                logging.error("Failed to analyze transcript")
                return None
        else:
            logging.error(
                "Could not proceed with analysis due to missing subtitle content."
            )
            return None


if __name__ == "__main__":
    main()
