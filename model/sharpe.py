import cv2
import numpy as np

# 이미지 읽기
img = cv2.imread('Booth2.bmp')

# 샤프닝 필터 적용
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
sharpened = cv2.filter2D(img, -1, kernel)

cv2.imwrite('Booth2_sharp.bmp', sharpened)
