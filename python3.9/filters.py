# filters.py
import cv2
import numpy as np
from headband import headband_filter
from constants import EFFECT_CARTOONIFY, EFFECT_PENCIL_SKETCH, EFFECT_VINTAGE, EFFECT_HEADBAND

filters = {}

def register_filter(effect_id):
    def decorator(func):
        filters[effect_id] = func
        return func
    return decorator

@register_filter(EFFECT_CARTOONIFY)
def cartoonify_filter(frame):
    cartoon_image = cv2.bilateralFilter(frame, d=9, sigmaColor=75, sigmaSpace=75)
    gray = cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
    cartoon = cv2.bitwise_and(cartoon_image, cartoon_image, mask=edges)
    return cartoon

@register_filter(EFFECT_PENCIL_SKETCH)
def pencil_sketch_filter(frame):
    sketch_gray, sketch_color = cv2.pencilSketch(frame, sigma_s=30, sigma_r=0.04, shade_factor=0.02)
    return sketch_color

@register_filter(EFFECT_VINTAGE)
def vintage_filter(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    retro_filter = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
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

@register_filter(EFFECT_HEADBAND)
def headband_filter_wrapper(frame, predictor, rect):
    return headband_filter(frame, predictor, rect)
