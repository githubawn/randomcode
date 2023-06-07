#input file should be "We Are Here.mp4", download from https://www.youtube.com/watch?v=wp_BsqgWbb4 and rename
#red teaming an example of PsyCrypto https://qri.org/blog/psycrypto-contest

import cv2
import numpy as np

def apply_scanner_effect(video_path, output_path):
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Prepare the VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Calculate the number of frames to delay before fading and the duration of the fade
    fade_start = int(fps * 1.5)  # start fading after 1.5 seconds
    fade_duration = int(fps * 0.5)  # fade over 0.5 seconds
    trail_length = fade_start + fade_duration

    # List of previous frames
    previous_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Keep only the white pixels
        white = np.where(gray > 200, 255, 0)

        previous_frames.append(white)

        # If the list of previous frames gets too long, remove the oldest frame
        if len(previous_frames) > trail_length:
            previous_frames.pop(0)

        # Calculate the accumulated frame
        accumulated_frame = np.zeros_like(white)
        for i, prev in enumerate(previous_frames):
            # If the frame is older than the fade start, start fading it
            if i < len(previous_frames) - fade_start:
                fade_factor = (len(previous_frames) - i) / fade_duration
                prev = prev * fade_factor

            accumulated_frame = np.maximum(accumulated_frame, prev)

        # Convert back to BGR for the VideoWriter
        output = cv2.cvtColor(accumulated_frame.astype(np.uint8), cv2.COLOR_GRAY2BGR)

        out.write(output)

    cap.release()
    out.release()

# Apply the scanner effect and save the output
apply_scanner_effect('We Are Here.mp4', 'outputchloe21e8灭绝公主.mp4')
