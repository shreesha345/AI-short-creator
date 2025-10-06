import os

# first to run the Downloader.
os.system("python video_downloader.py")
os.system("python transcript_analysis.py")
os.system("python video_cutter.py")
os.system("python face.py")
os.system("python last_edit.py")
os.remove("output/best_video_1.mp4")
os.remove("output/best_video_3.mp4")
os.system("python process.py")
