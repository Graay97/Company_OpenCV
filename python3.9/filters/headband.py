# headband.py

import cv2
import numpy as np
from .base import register_filter
from config import EFFECT_HEADBAND, RESOURCES_DIR
import os

def headband_filter(frame, predictor, rect, gray=None):
    """머리띠 필터를 적용하는 함수
    
    Args:
        frame: 원본 이미지
        predictor: dlib 얼굴 랜드마크 predictor
        rect: 감지된 얼굴 영역
        gray: 회색조 이미지 (선택적)
    
    Returns:
        필터가 적용된 이미지
    """
    if gray is None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    landmarks = predictor(gray, rect)
    
    # 눈 위치 계산
    left_eye = (landmarks.part(36).x, landmarks.part(36).y)
    right_eye = (landmarks.part(45).x, landmarks.part(45).y)
    
    eye_distance = right_eye[0] - left_eye[0]
    
    try:
        headband_path = os.path.join(RESOURCES_DIR, 'headband_picture', 'mickey_500.png')
        headband_img = cv2.imread(headband_path, -1)
        if headband_img is None:
            raise FileNotFoundError(f"머리띠 이미지 파일({headband_path})을 찾을 수 없습니다.")
    except FileNotFoundError as e:
        print(e)
        return frame

    # 머리띠 크기 조정
    headband_width = int(eye_distance * 2.5)
    headband_height = int(headband_img.shape[0] * (headband_width / headband_img.shape[1]))
    headband_resized = cv2.resize(headband_img, (headband_width, headband_height))
    
    # 머리띠 위치 계산
    top_left = (
        left_eye[0] - int(eye_distance / 2) - int(headband_width * 0.1),
        left_eye[1] - int(headband_height * 1)
    )
    
    # 이미지 경계 확인
    y1, y2 = max(top_left[1], 0), min(top_left[1] + headband_height, frame.shape[0])
    x1, x2 = max(top_left[0], 0), min(top_left[0] + headband_width, frame.shape[1])
    
    # 크기 조정된 머리띠 이미지 자르기
    y_offset = y1 - top_left[1]
    x_offset = x1 - top_left[0]
    headband_height_cropped = y2 - y1
    headband_width_cropped = x2 - x1
    
    if y_offset >= headband_resized.shape[0] or x_offset >= headband_resized.shape[1]:
        return frame
        
    headband_resized_cropped = headband_resized[
        max(0, y_offset):min(y_offset + headband_height_cropped, headband_resized.shape[0]),
        max(0, x_offset):min(x_offset + headband_width_cropped, headband_resized.shape[1])
    ]
    
    if headband_resized_cropped.size == 0:
        return frame
        
    # 알파 채널을 사용한 블렌딩
    alpha_s = headband_resized_cropped[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s
    
    for c in range(0, 3):
        frame[y1:y1+headband_resized_cropped.shape[0], 
              x1:x1+headband_resized_cropped.shape[1], c] = (
            alpha_s * headband_resized_cropped[:, :, c] +
            alpha_l * frame[y1:y1+headband_resized_cropped.shape[0], 
                          x1:x1+headband_resized_cropped.shape[1], c]
        )
    
    return frame

