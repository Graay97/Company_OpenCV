import numpy as np
import cv2

def overlay(image, x, y, w, h, overlay_image):
    # 오버레이할 이미지 크기 조정 (w, h에 맞춰서)
    overlay_resized = cv2.resize(overlay_image, (w, h))
    
    print("Resized overlay image shape:", overlay_resized.shape)  # 디버깅용 출력: 리사이즈된 이미지 크기

    # 알파 채널 추출 (이미지가 BGRA일 때만)
    if overlay_resized.shape[2] == 4:
        alpha = overlay_resized[:, :, 3] / 255.0  # 알파 채널 (0-1 사이로 정규화)
    else:
        alpha = np.ones(overlay_resized.shape[:2], dtype=float)  # 알파 채널이 없으면 완전 불투명 처리

    # 이미지 크기와 오버레이 이미지 크기 범위 체크
    y1, y2 = max(0, y - h), min(image.shape[0], y + h)
    x1, x2 = max(0, x - w), min(image.shape[1], x + w)

    # 오버레이 이미지 크기와 영역 크기 맞추기
    overlay_resized_cropped = overlay_resized[:y2 - y1, :x2 - x1]  # 리사이즈된 이미지 잘라내기
    alpha_cropped = alpha[:y2 - y1, :x2 - x1]  # 알파 채널 잘라내기

    # 이미지 영역에 오버레이 이미지 삽입
    for c in range(0, 3):  # 0, 1, 2는 BGR 채널
        # 알파 채널에 따라 이미지 오버레이
        image[y1:y2, x1:x2, c] = (overlay_resized_cropped[:, :, c] * alpha_cropped) + (image[y1:y2, x1:x2, c] * (1 - alpha_cropped))

    return image
