import os
import cv2
from .constants import COLORMAP_JET

# 프로젝트 루트 경로 설정
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 리소스 경로 설정
RESOURCES_DIR = os.path.join(PROJECT_ROOT, 'resources')

# 스크린샷 및 동영상 저장 디렉토리 설정
SCREENSHOTS_DIR = os.path.join(RESOURCES_DIR, 'screenshots')
VIDEOS_DIR = os.path.join(RESOURCES_DIR, 'videos')

# 랜드마크 모델 파일 경로
FACE_LANDMARK_MODEL = os.path.join(RESOURCES_DIR, 'shape_predictor_68_face_landmarks.dat')

# 카메라 설정
CAMERA_WIDTH = 1660
CAMERA_HEIGHT = 900

# 비디오 설정
VIDEO_FPS = 30
VIDEO_CODEC = 'DIVX'

# 필터 설정
CARTOON_BILATERAL_D = 9
CARTOON_SIGMA_COLOR = 75
CARTOON_SIGMA_SPACE = 75

PENCIL_SKETCH_SIGMA_S = 60          
PENCIL_SKETCH_SIGMA_R = 0.02
PENCIL_SKETCH_SHADE_FACTOR = 0.02

VINTAGE_ALPHA = 0.8               # 빈티지 효과 강도 증가
VINTAGE_BETA = 30                 # 밝기 약간 감소
VINTAGE_NOISE_SIGMA = 15          # 노이즈 감소
VINTAGE_SATURATION_FACTOR = 0.5   # 채도 더 감소

THREE_D_CANNY_THRESHOLD1 = 100        # Canny 엣지 검출의 첫 번째 임계값
THREE_D_CANNY_THRESHOLD2 = 200        # Canny 엣지 검출의 두 번째 임계값
THREE_D_SHADOW_WEIGHT = 0.8           # 그림자 강화 비율
THREE_D_HIGHLIGHT_WEIGHT = 1.2        # 하이라이트 강화 비율
THREE_D_DEPTH_COLOUR_MAP = cv2.COLORMAP_JET # 깊이 맵 컬러 맵
THREE_D_THREE_D_WEIGHT1 = 0.7         # 다층 이미지 효과의 첫 번째 가중치
THREE_D_THREE_D_WEIGHT2 = 0.3         # 다층 이미지 효과의 두 번째 가중치