import cv2
import numpy as np
import logging
from .base import register_filter
from config.constants import EFFECT_THREE_D
from config.settings import (
    THREE_D_CANNY_THRESHOLD1,
    THREE_D_CANNY_THRESHOLD2,
    THREE_D_SHADOW_WEIGHT,
    THREE_D_HIGHLIGHT_WEIGHT,
    THREE_D_DEPTH_COLOUR_MAP,
    THREE_D_THREE_D_WEIGHT1,
    THREE_D_THREE_D_WEIGHT2
)

@register_filter(EFFECT_THREE_D)
def three_d_effect_filter(frame):
    """
    입체 효과 필터를 적용하여 이미지에 깊이감을 부여합니다.
    
    Args:
        frame (numpy.ndarray): 입력 프레임
    
    Returns:
        numpy.ndarray: 입체 효과가 적용된 프레임
    """
    try:
        # 그레이스케일 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 깊이 맵 생성 (엣지 검출을 통해 깊이감을 표현)
        depth_map = cv2.Canny(gray, THREE_D_CANNY_THRESHOLD1, THREE_D_CANNY_THRESHOLD2)
        depth_map = cv2.GaussianBlur(depth_map, (5, 5), 0)  # 커널 크기 고정
        
        # 그림자 및 하이라이트 강화
        shadow = cv2.addWeighted(frame, THREE_D_SHADOW_WEIGHT, np.zeros_like(frame), 0, 50)  # 밝기 조정 값 고정
        highlight = cv2.addWeighted(shadow, THREE_D_HIGHLIGHT_WEIGHT, np.zeros_like(frame), 0, -30)  # 밝기 조정 값 고정
        
        # 깊이 맵을 컬러로 변환
        depth_colored = cv2.applyColorMap(depth_map, THREE_D_DEPTH_COLOUR_MAP)
        
        # 다층 이미지 효과 적용
        three_d = cv2.addWeighted(highlight, THREE_D_THREE_D_WEIGHT1, depth_colored, THREE_D_THREE_D_WEIGHT2, 0)
        
        return three_d
    except Exception as e:
        logging.error(f"3D 효과 적용 중 오류 발생: {e}", exc_info=True)
        return frame