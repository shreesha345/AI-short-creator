import os
from pytube import YouTube
from pydub import AudioSegment
import subprocess
import shutil


def download_video_with_audio(url, output_path='D:\\AI-video-maker\\final work\\raw_video'):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get all streams with both video and audio
        video_streams = yt.streams.filter(file_extension='mp4', progressive=True, subtype='mp4')

        if not video_streams:
            print("Error: No video streams available.")
            return None

        # Choose the stream with the highest resolution
        video_stream = video_streams.order_by('resolution').desc().first()

        if not video_stream:
            print("Error: No suitable video stream found.")
            return None

        # Ensure the filename is "video_with_audio.mp4"
        output_file_path = os.path.join(output_path, "video.mp4")
        print(f"Downloading video with audio: {yt.title} ({video_stream.resolution})")
        video_stream.download(output_path, filename='video.mp4')  # Enforce the filename
        print(f"Download completed! Saved as: {output_file_path}")

        return output_file_path

    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_audio_from_video(video_path, output_path):
    try:
        # Load the video clip
        video_clip = AudioSegment.from_file(video_path, format="mp4")

        # Export audio
        audio_file_path = os.path.join(output_path, 'audio.mp3')
        video_clip.export(audio_file_path, format="mp3")

        return audio_file_path

    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_subtitles(input_audio, output_path='D:\\AI-video-maker\\final work\\raw_video'):
    try:
        # Run the command to extract subtitles
        subtitle_path = os.path.join(output_path, 'subtitles.srt')
        command = f"stable-ts raw_video/audio.mp3 -o subtitles.srt --segment_level True --word_level False"
        subprocess.run(command, shell=True)
        print("Subtitle extraction completed!")
        source_path = 'D:\\AI-video-maker\\final work\\subtitles.srt'
        destination_path = 'D:\\AI-video-maker\\Final work\\raw_video'
        shutil.move(source_path, destination_path)
        print("file moved")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace 'your_video_url' with the actual URL of the YouTube video
    video_url = input("Enter the YouTube video URL: ")

    # Download the video with audio into the specified output path with the file name "video_with_audio.mp4"
    video_with_audio_path = download_video_with_audio(video_url)

    if video_with_audio_path:
        print(f"Video with audio saved at: {video_with_audio_path}")

        # Extract audio from the video
        extracted_audio_path = extract_audio_from_video(video_with_audio_path, os.path.dirname(video_with_audio_path))

        if extracted_audio_path:
            print(f"Extracted audio saved at: {extracted_audio_path}")

            # Extract subtitles from the audio
            extract_subtitles(extracted_audio_path)

            # Delete the audio file after subtitle extraction
            os.remove(extracted_audio_path)
            print("Audio file deleted.")
