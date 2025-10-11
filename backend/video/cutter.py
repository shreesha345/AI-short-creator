import json
import os

from moviepy.video.io.VideoFileClip import VideoFileClip

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
INPUT_VIDEO_PATH = os.path.join(DATA_DIR, "input", "raw_video", "video.mp4")
OUTPUT_DIR = os.path.join(DATA_DIR, "output", "clips")
JSON_FILE_PATH = os.path.join(DATA_DIR, "input", "main_part.json")


def cut_video(input_video_path, output_dir, json_file_path):
    """
    Cuts video into segments based on JSON configuration.

    Args:
        input_video_path (str): Path to input video file
        output_dir (str): Directory to save video clips
        json_file_path (str): Path to JSON file with segment information

    Returns:
        list: List of output file names if successful, empty list if failed
    """
    output_files = []
    video_clip = None

    try:
        if not os.path.exists(input_video_path):
            print(f"Error: Input video file not found: {input_video_path}")
            return []

        if not os.path.exists(json_file_path):
            print(f"Error: JSON file not found: {json_file_path}")
            return []

        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        if not isinstance(data, list):
            print("Error: JSON data should be a list of segments")
            return []

        if not data:
            print("Warning: No segments found in JSON file")
            return []

        video_clip = VideoFileClip(input_video_path)
        video_duration = video_clip.duration

        print(
            f"Processing {len(data)} segments from video (duration: {video_duration:.2f}s)"
        )

        for i, segment in enumerate(data, start=1):
            try:
                required_keys = ["start_time", "end_time", "description"]
                if not all(key in segment for key in required_keys):
                    print(f"Warning: Segment {i} missing required keys, skipping")
                    continue

                start_time = float(segment["start_time"])
                end_time = float(segment["end_time"])
                description = segment["description"]

                if start_time < 0 or end_time <= start_time:
                    print(f"Warning: Invalid timestamps for segment {i}, skipping")
                    continue

                if end_time > video_duration:
                    print(
                        f"Warning: End time {end_time}s exceeds video duration {video_duration:.2f}s for segment {i}"
                    )
                    end_time = video_duration

                output_file_name = f"video_{i}.mp4"
                output_file_path = os.path.join(output_dir, output_file_name)

                subclip = video_clip.subclipped(start_time, end_time)
                subclip.write_videofile(
                    output_file_path, codec="libx264", audio_codec="aac", logger=None
                )
                subclip.close()

                output_files.append(output_file_name)
                print(f"Segment {i}: {description}")
                print(f"Saved as: {output_file_path}")

            except Exception as e:
                print(f"Error processing segment {i}: {e}")
                continue

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error during video cutting: {e}")
        return []
    finally:
        if video_clip:
            video_clip.close()

    print(f"Successfully created {len(output_files)} video clips")
    return output_files


def main():
    """
    Main function to cut videos based on configuration.

    Returns:
        list: List of created video files
    """
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        return cut_video(INPUT_VIDEO_PATH, OUTPUT_DIR, JSON_FILE_PATH)
    except Exception as e:
        print(f"Error in main function: {e}")
        return []


if __name__ == "__main__":
    main()
