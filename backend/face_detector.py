import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
from concurrent.futures import ProcessPoolExecutor

import cv2
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
from mtcnn import MTCNN
from tqdm import tqdm

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
INPUT_DIR = os.path.join(DATA_DIR, "output", "clips")
OUTPUT_DIR = os.path.join(DATA_DIR, "output", "final_clips")

FACE_CHECK_INTERVAL = 10
CROP_RATIO = 9 / 16


def detect_face_center(frame: np.ndarray, detector: MTCNN) -> tuple[int, int] | None:
    """Detect face and return its center coordinates."""
    small_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
    faces = detector.detect_faces(small_frame)

    if faces and faces[0]["confidence"] > 0.9:
        box = faces[0]["box"]
        x, y, w, h = [coord / 0.3 for coord in box]
        return int(x + w / 2), int(y + h / 2)
    return None


def crop_frame_around_face(
    frame: np.ndarray,
    face_center: tuple[int, int],
    output_width: int,
    output_height: int,
) -> np.ndarray:
    """Crop frame around face center."""
    height, width = frame.shape[:2]
    face_x, face_y = face_center

    crop_x = max(0, min(face_x - output_width // 2, width - output_width))
    crop_y = max(0, min(face_y - output_height // 2, height - output_height))

    cropped = frame[crop_y : crop_y + output_height, crop_x : crop_x + output_width]
    return cv2.resize(cropped, (output_width, output_height))


def process_video(video_filename: str) -> str | None:
    """Process single video file."""
    try:
        video_path = os.path.join(INPUT_DIR, video_filename)
        output_path = os.path.join(OUTPUT_DIR, f"best_{video_filename}")

        video = VideoFileClip(video_path)
        detector = MTCNN()

        video_size = video.size
        if isinstance(video_size, (list, tuple)) and len(video_size) >= 2:
            width, height = int(video_size[0]), int(video_size[1])
        else:
            width, height = 1920, 1080
        output_width = int(height * CROP_RATIO)

        face_center = None
        for i, frame in enumerate(video.iter_frames()):
            if i > 50:
                break
            if i % 5 == 0:
                face_center = detect_face_center(frame, detector)
                if face_center:
                    break

        if not face_center:
            face_center = (width // 2, height // 2)

        processed_frames = []
        frame_count = 0

        for frame in video.iter_frames():
            if frame_count % FACE_CHECK_INTERVAL == 0:
                new_center = detect_face_center(frame, detector)
                if new_center:
                    face_center = new_center

            cropped_frame = crop_frame_around_face(
                frame, face_center, output_width, height
            )
            processed_frames.append(cropped_frame)
            frame_count += 1

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_fps = getattr(video, "fps", 30.0)
        fps_val = (
            float(video_fps)
            if isinstance(video_fps, (int, float)) and video_fps > 0
            else 30.0
        )
        out = cv2.VideoWriter(output_path, fourcc, fps_val, (output_width, height))

        for frame in processed_frames:
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(bgr_frame)

        out.release()
        video.close()

        print(f"Processed: {video_filename}")
        return video_filename

    except Exception as e:
        print(f"Failed to process {video_filename}: {e}")
        return None


def main(video_files: list[str]) -> list[str]:
    """Process multiple video files with face detection."""
    if not video_files:
        print("No video files to process")
        return []

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Processing {len(video_files)} videos with face detection...")

    successful_files = []
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = list(
            tqdm(
                executor.map(process_video, video_files),
                total=len(video_files),
                desc="Processing videos",
            )
        )

        successful_files = [f for f in results if f is not None]

    print(f"Successfully processed {len(successful_files)}/{len(video_files)} videos")
    return successful_files


if __name__ == "__main__":
    if os.path.exists(INPUT_DIR):
        video_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".mp4")]
        _ = main(video_files)
    else:
        print(f"Input directory not found: {INPUT_DIR}")
