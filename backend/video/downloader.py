import os
import subprocess

from pydub import AudioSegment
from pytube import YouTube

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
INPUT_DIR = os.path.join(DATA_DIR, "input", "raw_video")


def download_video_with_audio(url, output_path=INPUT_DIR):
    """Downloads a YouTube video and saves it to the specified path."""
    try:
        print(f"Ensuring output directory exists: {output_path}")
        os.makedirs(output_path, exist_ok=True)

        yt = YouTube(url)
        video_stream = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )

        if not video_stream:
            print("Error: No suitable progressive MP4 stream found.")
            return None

        output_file_path = os.path.join(output_path, "video.mp4")
        print(f"Downloading: {yt.title} ({video_stream.resolution})")
        video_stream.download(output_path, filename="video.mp4")
        print(f"Download completed! Saved as: {output_file_path}")
        return output_file_path

    except Exception as e:
        print(f"Error during video download: {e}")
        return None


def extract_audio_from_video(video_path, output_path=INPUT_DIR):
    """Extracts audio from a video file and saves it as an MP3."""
    try:
        video_clip = AudioSegment.from_file(video_path, format="mp4")
        audio_file_path = os.path.join(output_path, "audio.mp3")
        print(f"Extracting audio to: {audio_file_path}")
        video_clip.export(audio_file_path, format="mp3")
        return audio_file_path

    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None


def extract_subtitles(audio_path, output_path=INPUT_DIR):
    """Generates subtitles from an audio file using stable-ts."""
    try:
        if not os.path.exists(audio_path):
            print(f"Error: Audio file not found at {audio_path}")
            return

        subtitle_path = os.path.join(output_path, "subtitles.srt")

        relative_audio_path = os.path.relpath(audio_path, output_path)

        command = (
            f'stable-ts "{relative_audio_path}" -o "{os.path.basename(subtitle_path)}"'
        )

        print(f"Running subtitle extraction in '{output_path}'...")
        print(f"Command: {command}")

        subprocess.run(command, shell=True, check=True, cwd=output_path)

        print(f"Subtitle extraction completed! Saved as: {subtitle_path}")

    except Exception as e:
        print(f"Error extracting subtitles: {e}")


def main():
    """
    Main function to run the download pipeline.
    Gets the video URL from an environment variable.
    """
    video_url = os.getenv("YOUTUBE_URL")
    if not video_url:
        print("Error: YOUTUBE_URL environment variable not set. Please provide a URL.")
        return

    print(f"Starting download for URL: {video_url}")
    video_path = download_video_with_audio(video_url)
    if not video_path:
        return

    audio_path = extract_audio_from_video(video_path)
    if not audio_path:
        return

    extract_subtitles(audio_path)

    try:
        os.remove(audio_path)
        print("Temporary audio file deleted.")
    except OSError as e:
        print(f"Error deleting audio file: {e}")


if __name__ == "__main__":
    main()
