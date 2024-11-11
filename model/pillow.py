from PIL import Image, ImageEnhance

# 이미지 열기
img = Image.open('Booth2.bmp')

# 선명도, 대비 증가
enhancer = ImageEnhance.Sharpness(img)
img = enhancer.enhance(8.0)  # 선명도 증가
img.save('Booth2_pillow.bmp')
