import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 읽기
img = cv2.imread('stand.bmp')
img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

# CLAHE 적용
img_clahe = img_yuv.copy()
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
img_clahe[:,:,0] = clahe.apply(img_clahe[:,:,0])
img_clahe = cv2.cvtColor(img_clahe, cv2.COLOR_YUV2BGR)

# 이미지 저장
cv2.imwrite('stand_clahe.bmp', img_clahe)

# 이미지 표시
plt.figure(figsize=(15, 6)) # 그림의 가로 15 세로 6

# 원본 이미지
plt.subplot(2, 2, 1) # 2행 2열 서브플롯 인덱스1
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Before')

# CLAHE 적용 이미지
plt.subplot(2, 2, 2)
plt.imshow(cv2.cvtColor(img_clahe, cv2.COLOR_BGR2RGB))
plt.title('CLAHE')

# 원본 이미지 히스토그램
plt.subplot(2, 2, 3)
plt.hist(img.flatten(), bins=256, range=[0, 256], color='blue', alpha=0.5)
plt.title('Histogram - Before')

# CLAHE 적용 이미지 히스토그램
plt.subplot(2, 2, 4)
plt.hist(img_clahe.flatten(), bins=256, range=[0, 256], color='orange', alpha=0.5)
plt.title('Histogram - CLAHE')

plt.show()