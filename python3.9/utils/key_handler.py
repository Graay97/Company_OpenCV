# key_handler.py

import cv2
import os
from dataclasses import dataclass
from config import (
    EFFECT_NAMES, VIDEO_CODEC, VIDEO_FPS, CAMERA_WIDTH, CAMERA_HEIGHT,
    SCREENSHOTS_DIR, VIDEOS_DIR
)

@dataclass
class KeyInputResult:
    effect_type: int
    bRec: bool
    outputVideo: cv2.VideoWriter
    exit_signal: bool = False

def handle_key_input(key, effect_type, bRec, outputVideo, output_frame):
    # 디렉토리 생성 (존재하지 않을 경우)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)

    if ord('0') <= key <= ord('5'):
        effect_type = key - ord('0')
    elif key == ord('s'):
        filename = f"{EFFECT_NAMES.get(effect_type, 'Unknown')}_capture.jpg"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        try:
            cv2.imwrite(filepath, output_frame)
            print(f"이미지 캡처 완료: {filepath}")
        except Exception as e:
            print(f"이미지 캡처 실패: {e}")
    elif key == ord('r'):
        if not bRec:
            try:
                video_filename = f"Video_{len(os.listdir(VIDEOS_DIR)) + 1}.avi"
                video_path = os.path.join(VIDEOS_DIR, video_filename)
                outputVideo = cv2.VideoWriter(
                    video_path, 
                    cv2.VideoWriter_fourcc(*VIDEO_CODEC), 
                    VIDEO_FPS, 
                    (CAMERA_WIDTH, CAMERA_HEIGHT)
                )
                bRec = True
                print(f"녹화 시작: {video_path}")
            except Exception as e:
                print(f"동영상 녹화 시작 실패: {e}")
        else:
            try:
                outputVideo.release()
                outputVideo = None
                bRec = False
                print("녹화 중지")
            except Exception as e:
                print(f"동영상 녹화 중지 실패: {e}")
    elif key == ord('q'):
        return KeyInputResult(effect_type, bRec, outputVideo, exit_signal=True)
    return KeyInputResult(effect_type, bRec, outputVideo)
