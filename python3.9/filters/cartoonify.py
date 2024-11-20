import cv2
from .base import register_filter
from config import EFFECT_CARTOONIFY

@register_filter(EFFECT_CARTOONIFY)
def cartoonify_filter(frame):
    cartoon_image = cv2.bilateralFilter(frame, d=9, sigmaColor=75, sigmaSpace=75)
    gray = cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
    cartoon = cv2.bitwise_and(cartoon_image, cartoon_image, mask=edges)
    return cartoon