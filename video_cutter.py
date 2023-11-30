import json
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
def cut_video(input_video_path, output_dir, json_file_path):
    # Load the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Open the input video
    video_clip = VideoFileClip(input_video_path)

    # Cut the video into parts based on the time intervals in the JSON file
    for i, segment in enumerate(data['combined_response'], start=1):
        start_time = segment['start_time']
        end_time = segment['end_time']
        duration = segment['duration']
        description = segment['description']

        # Set the output file name
        output_file_name = f"video_{i}.mp4"
        output_file_path = os.path.join(output_dir, output_file_name)

        # Extract the subclip
        subclip = video_clip.subclip(start_time, end_time)

        # Write the subclip to the output file
        subclip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

        print(f"Segment {i}: {description}")
        print(f"Saved as: {output_file_path}")

    # Close the video clip
    video_clip.close()

if __name__ == "__main__":
    # Replace 'your_input_video.mp4', 'output_directory', and 'your_json_file.json' with your actual file paths
    input_video_path = 'raw_video/video.mp4'
    output_directory = 'Clips'
    json_file_path = 'main_part.json'

    # Make sure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Cut the video based on the JSON file
    cut_video(input_video_path, output_directory, json_file_path)
