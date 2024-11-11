# filters.py
import cv2
import dlib
import numpy as np

# Dlib 얼굴 감지기 및 랜드마크 감지기 초기화 (메인 코드에서 초기화할 경우 함수 인자로 받아 사용)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Cartoonify 효과
def cartoonify_filter(frame):
    cartoon_image = cv2.bilateralFilter(frame, d=9, sigmaColor=75, sigmaSpace=75)
    gray = cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
    cartoon = cv2.bitwise_and(cartoon_image, cartoon_image, mask=edges)
    return cartoon

# Pencil Sketch 효과
def pencil_sketch_filter(frame):
    sketch_gray, sketch_color = cv2.pencilSketch(frame, sigma_s=45, sigma_r=0.04, shade_factor=0.03)
    return sketch_color

# Vintage (레트로) 효과
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

# 얼굴 특징 확대/축소 함수
def exaggerate_features(frame, eye_left, eye_right, new_eye_distance, nose, new_nose_distance):
    # 눈 간 거리 확장
    frame = cv2.line(frame, eye_left, eye_right, (0, 255, 0), 3)
    
    # 코 확대 (단순히 코 위치를 기준으로 처리)
    # 실제로는 얼굴 부위 왜곡을 적용할 수 있도록 구현
    frame = cv2.circle(frame, nose, int(new_nose_distance), (255, 0, 0), 2)
    
    return frame

# 필터 딕셔너리
filters = {
    1: cartoonify_filter,
    2: pencil_sketch_filter,
    3: vintage_filter
}
