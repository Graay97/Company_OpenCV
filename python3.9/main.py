# main.py
import cv2
from filters import filters
from key_handler import handle_key_input
from face_utils import initialize_face_detectors
from constants import EFFECT_NORMAL, EFFECT_HEADBAND
from headband import headband_filter

detector, predictor = initialize_face_detectors()
effect_type = EFFECT_NORMAL
bRec = False
outputVideo = None

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("카메라 초기화 실패")
    exit()

def apply_filters(frame, effect_type, flip=True):
    if flip:
        frame = cv2.flip(frame, 1)
    
    if effect_type == EFFECT_HEADBAND:
        if predictor is None or detector is None:
            return frame
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        if len(faces) > 0:
            for face in faces:
                frame = headband_filter(frame, predictor, face, gray)
        return frame

    return filters.get(effect_type, lambda x: x)(frame)


while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 읽기 실패")
        break

    output_frame = apply_filters(frame, effect_type)
    cv2.imshow("실시간 필터 적용", output_frame)

    key = cv2.waitKey(1) & 0xFF
    if key != 255:
        result = handle_key_input(key, effect_type, bRec, outputVideo, output_frame)
        
        if result.exit_signal:
            print("종료합니다.")
            break

        effect_type, bRec, outputVideo = result.effect_type, result.bRec, result.outputVideo

    if bRec and outputVideo is not None:
        outputVideo.write(output_frame)

# 종료 전 정리 작업을 명시적으로 수행
cv2.waitKey(1)  # 추가: 마지막 프레임 처리를 위한 대기
cap.release()
if outputVideo is not None:
    outputVideo.release()
cv2.destroyAllWindows()
cv2.waitKey(1)  # 추가: 모든 창이 제대로 닫힐 때까지 대기
