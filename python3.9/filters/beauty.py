import cv2
import numpy as np
from .base import register_filter
from config import EFFECT_BEAUTY

@register_filter(EFFECT_BEAUTY)
def beauty_filter(frame):
    """
    강화된 뷰티 필터 - 잡티 제거 효과 추가
    """
    # 1. 피부 톤 보정
    frame_ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
    y, cr, cb = cv2.split(frame_ycrcb)
    
    # 밝기 채널 향상
    y = cv2.add(y, 25)
    
    # 2. 피부 마스크 생성
    skin_min = np.array([0, 133, 77])
    skin_max = np.array([255, 173, 127])
    skin_mask = cv2.inRange(frame_ycrcb, skin_min, skin_max)
    
    # 마스크 정제
    kernel = np.ones((3,3), np.uint8)
    skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=1)
    skin_mask = cv2.GaussianBlur(skin_mask, (3,3), 0)
    
    # 3. 잡티 제거를 위한 처리
    # 작은 크기의 양방향 필터로 디테일 보존하면서 잡티 제거
    smooth1 = cv2.bilateralFilter(frame, 5, 50, 50)
    
    # 중간 크기의 양방향 필터로 피부 톤 균일화
    smooth2 = cv2.bilateralFilter(frame, 7, 55, 55)
    
    # 두 필터 결과 블렌딩
    beauty = cv2.addWeighted(smooth1, 0.6, smooth2, 0.4, 0)
    
    # 4. 전체적인 톤 보정
    beauty_hsv = cv2.cvtColor(beauty, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(beauty_hsv)
    s = cv2.add(s, 8)  # 채도 약간 증가
    v = cv2.add(v, 5)  # 명도 약간 증가
    beauty_hsv = cv2.merge([h, s, v])
    beauty = cv2.cvtColor(beauty_hsv, cv2.COLOR_HSV2BGR)
    
    # 5. 피부 영역만 합성
    skin_mask_3d = cv2.cvtColor(skin_mask, cv2.COLOR_GRAY2BGR) / 255.0
    
    # 자연스러운 블렌딩
    result = frame * (1 - skin_mask_3d * 0.75) + beauty * (skin_mask_3d * 0.75)
    
    # 6. 전체적인 밝기와 대비 미세 조정
    result = cv2.convertScaleAbs(result, alpha=1.05, beta=5)
    
    # 7. 선명도 약간 증가
    sharpen_kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    result = cv2.filter2D(result, -1, sharpen_kernel)
    
    return result.astype(np.uint8)
    