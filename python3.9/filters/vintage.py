import cv2
import numpy as np
from .base import register_filter
from config import EFFECT_VINTAGE

@register_filter(EFFECT_VINTAGE)
def vintage_filter(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    retro_filter = np.array([[0.7, 0.3, 0.2], 
                            [0.2, 0.7, 0.1], 
                            [0.1, 0.3, 0.7]])
    frame = cv2.transform(frame, retro_filter)
    frame = np.clip(frame, 0, 255)
    noise = np.random.normal(0, 10, frame.shape)
    frame = frame + noise
    frame = np.clip(frame, 0, 255)
    frame = cv2.convertScaleAbs(frame, alpha=0.85, beta=30)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    hsv[..., 1] = hsv[..., 1] * 0.8
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    frame = np.uint8(frame)
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)