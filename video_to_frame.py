import cv2
import os
import hashlib
import sys

def hash_frame(frame):
    """Convert frame to grayscale and return its hash."""
    resized = cv2.resize(frame, (64, 64))  # Resize to reduce noise
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    return hashlib.md5(gray).hexdigest()

def extract_unique_frames(video_path, output_dir="unique_frames"):
    try:
        # Validate input file
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"File not found: {video_path}")
        if not video_path.lower().endswith(".mp4"):
            raise ValueError("Invalid file type. Please provide an MP4 file.")

        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError("Failed to open the video file. It might be corrupted or unsupported.")

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        frame_id = 0
        saved = 0
        prev_hash = None

        print("Processing video. This might take a while...")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            current_hash = hash_frame(frame)

            if current_hash != prev_hash:
                frame_filename = os.path.join(output_dir, f"frame_{saved:04d}.jpg")
                cv2.imwrite(frame_filename, frame)
                saved += 1
                prev_hash = current_hash

            frame_id += 1

        cap.release()
        print(f"\n✅ Done! Extracted {saved} unique frames out of {frame_id} total frames.")
        print(f"📂 Saved in folder: {os.path.abspath(output_dir)}")

    except FileNotFoundError as fnf_err:
        print(f"❌ Error: {fnf_err}")
    except ValueError as val_err:
        print(f"❌ Error: {val_err}")
    except IOError as io_err:
        print(f"❌ Error: {io_err}")
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("=== Unique Frame Extractor ===")
    video_path = input("Enter path to MP4 file: ").strip()
    output_dir = input("Enter output folder name (or press Enter to use default 'unique_frames'): ").strip()

    if not output_dir:
        output_dir = "unique_frames"

    extract_unique_frames(video_path, output_dir)

