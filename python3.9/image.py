import cv2
import dlib
import numpy as np

def overlay(image, x, y, w, h, overlay_image):  # 대상 이미지 (3채널), x, y 좌표, width, height, 덮어씌울 이미지 (4채널)
    if overlay_image.shape[2] == 4:  # 4채널 (BGRA)일 경우
        alpha = overlay_image[:, :, 3]  # 알파 채널(BGRA의 4번째 채널)
        mask_image = alpha / 255.0  # 0 ~ 255 -> 255 로 나누면 0 ~ 1 사이의 값 (1: 불투명, 0: 완전 투명)
    else:  # 3채널 (BGR)일 경우
        mask_image = 1  # 완전히 불투명

    for c in range(0, 3):  # channel BGR
        # 원본 이미지와 덮어씌운 이미지의 알파값을 고려하여 결합
        image[y-h:y+h, x-w:x+w, c] = (overlay_image[:, :, c] * mask_image) + (image[y-h:y+h, x-w:x+w, c] * (1 - mask_image))

# dlib 얼굴 인식 및 얼굴 특징점 추적기를 설정합니다.
detector = dlib.get_frontal_face_detector()  # 얼굴 인식기
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # 얼굴 68개 특징점 예측기

# 웹캠 열기
cap = cv2.VideoCapture(0)

# 웹캠 해상도 설정 (1920x1080)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# 이미지 불러오기
image_right_eye = cv2.imread('right_eye.png', cv2.IMREAD_UNCHANGED)  # 100 x 100 (4채널로 읽기)
image_left_eye = cv2.imread('left_eye.png', cv2.IMREAD_UNCHANGED)  # 100 x 100 (4채널로 읽기)
image_nose = cv2.imread('nose.png', cv2.IMREAD_UNCHANGED)  # 300 x 100 (4채널로 읽기)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # 성능 향상을 위해 이미지를 쓰기 불가능하게 설정하여 참조로 전달
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 얼굴 인식
    faces = detector(gray)

    for face in faces:
        # 얼굴 영역을 추출합니다.
        landmarks = predictor(gray, face)  # 얼굴 특징점 추출

        # 68개 특징점에서 오른쪽 눈, 왼쪽 눈, 코 끝 좌표를 가져옵니다.
        right_eye = (landmarks.part(36).x, landmarks.part(36).y)  # 오른쪽 눈
        left_eye = (landmarks.part(45).x, landmarks.part(45).y)  # 왼쪽 눈
        nose_tip = (landmarks.part(30).x, landmarks.part(30).y)  # 코 끝

        # 각 특징에 이미지 덧씌우기
        overlay(image, *right_eye, 50, 50, image_right_eye)
        overlay(image, *left_eye, 50, 50, image_left_eye)
        overlay(image, *nose_tip, 150, 50, image_nose)

    # 좌우 반전
    image = cv2.flip(image, 1)

    # 화면 크기 변경 (1280x720)
    image_resized = cv2.resize(image, (1280, 720))

    # 웹캠 화면을 반전시켜서 셀카 모드로 출력
    cv2.imshow('dlib Face Detection', image_resized)

    if cv2.waitKey(1) == ord('q'):  # 'q' 키를 눌러서 종료
        break

cap.release()
cv2.destroyAllWindows()
