import cv2
from .base import register_filter
from config import EFFECT_PENCIL_SKETCH

@register_filter(EFFECT_PENCIL_SKETCH)
def pencil_sketch_filter(frame):
    sketch_gray, sketch_color = cv2.pencilSketch(frame, sigma_s=30, sigma_r=0.04, shade_factor=0.02)
    return sketch_color