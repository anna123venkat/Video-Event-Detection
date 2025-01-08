import cv2
import os

def split_video_into_frames(video_path, output_folder, num_frames=80):
    cap = cv2.VideoCapture(video_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    step_size = total_frames // num_frames
    print(total_frames)
    print(step_size)

    frame_count = 0
    current_frame = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if current_frame % step_size == 0:
            frame_name = f"frame_{frame_count:04d}.png"
            frame_path = os.path.join(output_folder, frame_name)
            cv2.imwrite(frame_path, frame)
            frame_count += 1

        current_frame += 1

        if frame_count == num_frames:
            break

    cap.release()
