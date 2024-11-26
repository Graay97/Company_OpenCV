# constants.py

EFFECT_NORMAL = 0
EFFECT_CARTOONIFY = 1  
EFFECT_VINTAGE = 2
EFFECT_HEADBAND = 3
EFFECT_BEAUTY = 4

EFFECT_NAMES = {
    EFFECT_NORMAL: "Normal",
    EFFECT_CARTOONIFY: "Cartoonify",
    EFFECT_VINTAGE: "Vintage",
    EFFECT_HEADBAND: "Headband",
    EFFECT_BEAUTY: "Beauty",
}

import cv2

# 컬러 맵 상수 추가
COLORMAP_JET = cv2.COLORMAP_JET
COLORMAP_HOT = cv2.COLORMAP_HOT
# 필요한 다른 컬러 맵도 추가 가능
