# key_handler.py

import cv2
import os
from dataclasses import dataclass
from config import (
    EFFECT_NAMES, VIDEO_CODEC, VIDEO_FPS, CAMERA_WIDTH, CAMERA_HEIGHT,
    EFFECT_NORMAL, EFFECT_CARTOONIFY, EFFECT_VINTAGE, EFFECT_HEADBAND,
    EFFECT_BEAUTY,
    SCREENSHOTS_DIR, VIDEOS_DIR
)
import logging

logger = logging.getLogger(__name__)

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

    if ord('0') <= key <= ord('4'):
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
    elif key == ord('0'):
        logger.info("기본 화면으로 전환")
        return KeyInputResult(effect_type=EFFECT_NORMAL, bRec=bRec, outputVideo=outputVideo)
    elif key == ord('1'):
        logger.info("카툰 필터 적용")
        return KeyInputResult(effect_type=EFFECT_CARTOONIFY, bRec=bRec, outputVideo=outputVideo)
    elif key == ord('2'):
        logger.info("빈티지 필터 적용")
        return KeyInputResult(effect_type=EFFECT_VINTAGE, bRec=bRec, outputVideo=outputVideo)
    elif key == ord('3'):
        logger.info("헤드밴드 필터 적용")
        return KeyInputResult(effect_type=EFFECT_HEADBAND, bRec=bRec, outputVideo=outputVideo)
    elif key == ord('4'):
        logger.info("뷰티 필터 적용")
        return KeyInputResult(effect_type=EFFECT_BEAUTY, bRec=bRec, outputVideo=outputVideo)
    return KeyInputResult(effect_type, bRec, outputVideo)
