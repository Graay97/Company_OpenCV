import os

# 프로젝트 루트 경로 설정
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 리소스 경로 설정
RESOURCES_DIR = os.path.join(PROJECT_ROOT, 'resources')

# 랜드마크 모델 파일 경로
FACE_LANDMARK_MODEL = os.path.join(RESOURCES_DIR, 'shape_predictor_68_face_landmarks.dat')

# 카메라 설정
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# 비디오 설정
VIDEO_FPS = 30
VIDEO_CODEC = 'DIVX'

# 얼굴 인식 설정
FACE_LANDMARK_MODEL = 'shape_predictor_68_face_landmarks.dat'

# 필터 설정
CARTOON_BILATERAL_D = 9
CARTOON_SIGMA_COLOR = 75
CARTOON_SIGMA_SPACE = 75

PENCIL_SKETCH_SIGMA_S = 30
PENCIL_SKETCH_SIGMA_R = 0.04
PENCIL_SKETCH_SHADE_FACTOR = 0.02

VINTAGE_ALPHA = 0.7
VINTAGE_BETA = 50
VINTAGE_NOISE_SIGMA = 25
VINTAGE_SATURATION_FACTOR = 0.6