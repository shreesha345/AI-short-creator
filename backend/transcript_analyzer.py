import logging
import openai
import json
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up logging
logging.basicConfig(level=logging.INFO)

def read_subtitle_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def analyze_transcript(subtitle_file_path):
    # Read content from subtitle file
    subtitle_content = read_subtitle_file(subtitle_file_path)

    # Define the expected JSON format
    response_obj = [
        {
            "start_time": 0.0,
            "end_time": 55.26,
            "description": "main description",
            "duration": 55.26
        },
        {
            "start_time": 57.0,
            "end_time": 107.96,
            "description": "second main description",
            "duration": 50.96
        },
        {
            "start_time": 137.0,
            "end_time": 187.78,
            "description": "third main description",
            "duration": 50.78
        }
    ]

    # Process the entire content as one prompt
    prompt = f"This is a transcript of a video/podcast. Please identify the most viral sections from this part of the video, make sure they are more than 30 seconds in duration, Make sure you provide extremely accurate timestamps, respond only in this format {json.dumps(response_obj)}, I just want JSON as a Response (nothing else)  \n Here is the Transcription:\n{subtitle_content}"

    messages = [
        {"role": "system", "content": "You are a ViralGPT helpful assistant. You are a master at reading YouTube transcripts and identifying the most interesting parts and viral content from the podcasts making sure that it is more than 30 second and less then 58 second"},
        {"role": "user", "content": prompt}
    ]

    # Send the entire content as one prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        n=1,
        stop=None
    )

    # Extract and save the response as a JSON file
    combined_response = response.choices[0]['message']['content']
    with open('main_part.json', 'w') as json_file:
        json.dump({"combined_response": json.loads(combined_response)}, json_file, indent=2)  # Use indent to format the JSON nicely

    return json.loads(combined_response)

# Specify the path to your subtitle file
subtitle_file_path = 'raw_video/subtitles.srt'

# Analyze the transcript and save the output as JSON
analyze_transcript(subtitle_file_path)
