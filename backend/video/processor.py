import os

from moviepy import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
INPUT_DIR = os.path.join(DATA_DIR, "output", "final_clips")
OUTPUT_DIR = os.path.join(DATA_DIR, "output", "final_video")


def combine_clips(clips_directory, output_path):
    """
    Finds all video clips in a directory, sorts them, and combines them
    into a single output video file.

    Args:
        clips_directory (str): The path to the directory containing the video clips.
        output_path (str): The path to save the final concatenated video.
    """
    try:
        # Find all .mp4 files that start with 'best_'
        clip_files = [
            f
            for f in os.listdir(clips_directory)
            if f.endswith(".mp4") and f.startswith("best_")
        ]

        if not clip_files:
            print("Error: No processed clips found in the directory to combine.")
            return

        # Sort clips numerically based on the number in the filename (e.g., best_video_1.mp4)
        clip_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

        print(f"Found {len(clip_files)} clips to combine: {clip_files}")

        video_clips = [
            VideoFileClip(os.path.join(clips_directory, f)) for f in clip_files
        ]

        final_clip = concatenate_videoclips(video_clips, method="compose")

        print(f"Writing final video to: {output_path}")
        final_clip.write_videofile(
            output_path, codec="libx264", audio_codec="aac", logger="bar"
        )

        for clip in video_clips:
            clip.close()
        final_clip.close()

        print("Successfully created the final video.")

    except Exception as e:
        print(f"An error occurred during video processing: {e}")


def main():
    """
    Main function to orchestrate the final video creation process.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    final_video_path = os.path.join(OUTPUT_DIR, "final_video.mp4")

    combine_clips(INPUT_DIR, final_video_path)


if __name__ == "__main__":
    main()
