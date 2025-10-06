import os
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
import stable_whisper
import shutil
def extract_audio(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path, codec='mp3')
    video_clip.close()

def rename_and_copy(video_path, output_folder, caption_folder):
    video_name = os.path.basename(video_path)
    new_video_path = os.path.join(caption_folder, 'video.mp4')
    os.rename(video_path, new_video_path)
    return new_video_path

def run_stable_ts(audio_path, subtitle_path):
    subprocess.run(['stable-ts', audio_path, '-o', subtitle_path])

def main():
    input_folder = 'output'

    # Ensure the input folder exists
    if not os.path.exists(input_folder):
        print("The specified input folder does not exist.")
        return

    # Create necessary directories
    output_folder = input_folder
    caption_folder = os.path.join(os.path.dirname(input_folder), 'caption', 'public')
    os.makedirs(caption_folder, exist_ok=True)

    for video_file in os.listdir(input_folder):
        if video_file.endswith('.mp4') and video_file.startswith('best_video_'):
            video_path = os.path.join(input_folder, video_file)
            audio_path = os.path.join(caption_folder, 'audio.mp3')
            subtitle_path = os.path.join('D:\AI-video-maker\Final work', 'subtitles.srt')

            # Extract audio from the video
            extract_audio(video_path, audio_path)

            # Rename and copy the video to the required folder
            new_video_path = rename_and_copy(video_path, output_folder, caption_folder)

            # Run stable-ts command
            run_stable_ts(audio_path, subtitle_path)

            # Move subtitles to the caption/public folder
            shutil.move(subtitle_path, os.path.join(caption_folder, 'subtitles.srt'))

            # Run npm run build command
            os.chdir("D:\AI-video-maker\Final work\caption")
            os.system("npm run build")

            print(f"Processed video: {video_file}")

if __name__ == "__main__":
    main()