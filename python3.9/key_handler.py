# key_handler.py
import cv2
from dataclasses import dataclass
from constants import EFFECT_NAMES

@dataclass
class KeyInputResult:
    effect_type: int
    bRec: bool
    outputVideo: cv2.VideoWriter
    exit_signal: bool = False

def handle_key_input(key, effect_type, bRec, outputVideo, output_frame):
    if ord('0') <= key <= ord('4'):
        effect_type = key - ord('0')
    elif key == ord('s'):
        filename = f"{EFFECT_NAMES.get(effect_type, 'Unknown')}_capture.jpg"
        cv2.imwrite(filename, output_frame)
        print(f"이미지 캡처 완료: {filename}")
    elif key == ord('r'):
        if not bRec:
            outputVideo = cv2.VideoWriter('Video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30.0, (1280, 720))
            bRec = True
            print("녹화 시작")
        else:
            outputVideo.release()
            outputVideo = None
            bRec = False
            print("녹화 중지")
    elif key == ord('q'):
        return KeyInputResult(effect_type, bRec, outputVideo, exit_signal=True)
    return KeyInputResult(effect_type, bRec, outputVideo)
