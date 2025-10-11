import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from face_detector import main as detect_faces
from transcript_analyzer import main as analyze_transcript
from video.cutter import main as cut_video
from video.downloader import main as download_video
from video.processor import main as process_video

logging.basicConfig(level=logging.INFO)


def main():
    """Run the AI Short Creator pipeline."""
    print("Starting AI Short Creator Pipeline...")

    print("Downloading video...")
    download_video()

    print("Analyzing transcript...")
    analysis_result = analyze_transcript()
    if not analysis_result:
        raise RuntimeError("Transcript analysis failed")

    print("Cutting video clips...")
    cut_video_files = cut_video()
    if not cut_video_files:
        raise RuntimeError("No video clips generated")

    print("Detecting faces...")
    processed_files = detect_faces(cut_video_files)
    if not processed_files:
        raise RuntimeError("Face detection failed")

    print("Processing final video...")
    process_video()

    print("Pipeline complete! Check 'data/output/final_video' for results.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Pipeline failed: {e}")
        sys.exit(1)
