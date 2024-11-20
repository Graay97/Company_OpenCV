import cv2
import numpy as np
from .base import register_filter
from config import EFFECT_VINTAGE

@register_filter(EFFECT_VINTAGE)
def vintage_filter(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    retro_filter = np.array([[0.393, 0.769, 0.189], 
                            [0.349, 0.686, 0.168], 
                            [0.272, 0.534, 0.131]])
    frame = cv2.transform(frame, retro_filter)
    frame = np.clip(frame, 0, 255)
    noise = np.random.normal(0, 25, frame.shape)
    frame = frame + noise
    frame = np.clip(frame, 0, 255)
    frame = cv2.convertScaleAbs(frame, alpha=0.7, beta=50)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    hsv[..., 1] = hsv[..., 1] * 0.6
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    frame = np.uint8(frame)
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)