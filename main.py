from utils.video_downloader import download_video
from models.transcript_analysis import analyze_transcript
from utils.video_cutter import start_cut_video
from utils.face import detect_main
from utils.last_edit import finalize_edit
from utils.process import post_process
import os

def main():
    download_video()
    # Specify the path to your subtitle file
    subtitle_file_path = 'raw_video/subtitles.srt'
    # Analyze the transcript and save the output as JSON
    analyze_transcript(subtitle_file_path)
    analyze_transcript()
    start_cut_video()
    detect_main()
    finalize_edit()

    for file in ["output/best_video_1.mp4", "output/best_video_3.mp4"]:
        if os.path.exists(file):
            os.remove(file)

    post_process()

if __name__ == "__main__":
    main()