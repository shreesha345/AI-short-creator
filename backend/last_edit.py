# Import the os and cv2 modules
import os
import cv2

# Define the file name and extension as a string variable
file_name = "D:\\AI-video-maker\\Final work\\caption\\src\\Root.tsx"

# Open the file in the output directory with the given file name and extension in read mode
with open(file_name, "r") as f:
    # Read the text from the file
    text = f.read()

# Create a video object using cv2.VideoCapture and the video file name
video = cv2.VideoCapture("D:\\AI-video-maker\\Final work\\output\\best_video_2.mp4")

# Get the frame rate or frames per second of the video
frame_rate = video.get(cv2.CAP_PROP_FPS)

# Get the total number of frames in the video
total_num_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

# Calculate the duration of the video in seconds by dividing the total number of frames by the frame rate
duration = total_num_frames / frame_rate

# Round the duration to the nearest integer
duration = round(duration)

# Replace the durationInSeconds value in the text with the calculated duration
text = text.replace("durationInSeconds: 51", f"durationInSeconds: {duration}")

# Open the file in the output directory with the given file name and extension in write mode
with open(file_name, "w") as f:
    # Write the updated text to the file
    f.write(text)

# Print a message to indicate the file has been updated
print(f"File {file_name} has been updated with the duration of the video.")
