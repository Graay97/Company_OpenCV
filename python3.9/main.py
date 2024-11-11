# main.py
import cv2
from filters import filters
from key_handler import handle_key_input

# 초기화
effect_type = 0
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
def apply_filters(frame, effect_type):
    frame = cv2.flip(frame, 1)
    return filters.get(effect_type, lambda x: x)(frame)  # 필터 적용

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
