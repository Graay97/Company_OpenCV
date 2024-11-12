# main.py

# 필터 효과 상수 정의
EFFECT_NORMAL = 0
EFFECT_CARTOONIFY = 1
EFFECT_PENCIL_SKETCH = 2
EFFECT_VINTAGE = 3

import cv2
from filters import filters
from key_handler import handle_key_input

# 초기화
effect_type = EFFECT_NORMAL  # "Normal" 필터로 초기화
bRec = False
outputVideo = None

# 카메라 초기화
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("카메라 초기화 실패")
    exit()

# 필터 적용 함수
def apply_filters(frame, effect_type, flip=True):
    """
    주어진 프레임에 필터를 적용하고 선택적으로 좌우 반전을 처리합니다.

    :param frame: 입력 이미지 프레임
    :param effect_type: 적용할 필터의 유형
    :param flip: 좌우 반전 여부 (기본값 True)
    :return: 필터가 적용된 이미지 프레임
    """
    if flip:
        frame = cv2.flip(frame, 1)  # 좌우 반전
    return filters.get(effect_type, lambda x: x)(frame)

# 실시간 프레임 처리
while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 읽기 실패")
        break

    output_frame = apply_filters(frame, effect_type)
    cv2.imshow("실시간 필터 적용", output_frame)

    # 키보드 입력 처리
    key = cv2.waitKey(1) & 0xFF
    if key != 255:  # 키 입력이 있을 때만
        result = handle_key_input(key, effect_type, bRec, outputVideo, output_frame)
        if result is None:  # 종료 신호
            break
        effect_type, bRec, outputVideo = result

    # 녹화 중일 경우 현재 프레임을 비디오 파일에 저장
    if bRec and outputVideo is not None:
        outputVideo.write(output_frame)

# 자원 해제
cap.release()
if outputVideo is not None:
    outputVideo.release()
cv2.destroyAllWindows()
