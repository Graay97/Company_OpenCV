import cv2
import os

# 원본 이미지 폴더와 CLAHE 적용 이미지 저장 폴더 경로
input_folder = 'C:/Users/User/Documents/000.randering'  # 원본 이미지 폴더 경로
output_folder = 'C:/Users/User/Documents/001.clahe'  # 저장할 폴더 경로

# 저장 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 모든 이미지 파일에 대해 CLAHE 적용
for filename in os.listdir(input_folder):
    # 이미지 파일 확인 (jpg, png 등 필요한 확장자 추가)
    if filename.endswith(('.bmp', '.jpg', '.png')):
        # 이미지 읽기
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        # CLAHE 적용
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
        img_clahe = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        # CLAHE 이미지 저장
        output_path = os.path.join(output_folder, filename)  # 원본 파일 이름 유지
        cv2.imwrite(output_path, img_clahe)
        print(f"{filename} 처리 및 저장 완료")

print("모든 이미지 CLAHE 적용 및 저장 완료!")