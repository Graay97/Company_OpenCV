# main.py
import cv2
from filters import filters
from filters.headband import headband_filter
from utils import handle_key_input
from utils import initialize_face_detectors
from config import (
    EFFECT_NORMAL, EFFECT_HEADBAND,
    CAMERA_WIDTH, CAMERA_HEIGHT,
    VIDEO_FPS, VIDEO_CODEC
)
from utils.logger import MainLogger, FaceLogger
from exceptions import CameraInitError, CameraReadError, FilterApplyError

logger = MainLogger.get_logger()
face_logger = FaceLogger.get_logger()

logger.info("프로그램 시작")

try:
    logger.debug("얼굴 감지기 초기화 시도")
    detector, predictor = initialize_face_detectors()
    face_detection_enabled = True
    logger.info("얼굴 감지기 초기화 성공")
except Exception as e:
    logger.error(f"얼굴 감지기 초기화 실패: {e}")
    detector, predictor = None, None
    face_detection_enabled = False

effect_type = EFFECT_NORMAL
bRec = False
outputVideo = None

# 카메라 초기화
try:
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    if not cap.isOpened():
        raise CameraInitError()
except Exception as e:
    logger.error(f"카메라 초기화 실패: {str(e)}")
    exit(1)

def apply_filters(frame, effect_type, flip=True):
    try:
        if flip:
            frame = cv2.flip(frame, 1)
        
        if effect_type == EFFECT_HEADBAND:
            if not face_detection_enabled:
                logger.warning("얼굴 감지 기능을 사용할 수 없습니다")
                return frame
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            logger.debug("얼굴 감지 시도")
            faces = detector(gray)
            logger.debug(f"감지된 얼굴 수: {len(faces)}")
            
            if len(faces) > 0:
                for face in faces:
                    frame = headband_filter(frame, predictor, face, gray)
            return frame

        return filters.get(effect_type, lambda x: x)(frame)
    except Exception as e:
        logger.error(f"필터 적용 중 오류 발생: {e}", exc_info=True)
        return frame


while True:
    try:
        ret, frame = cap.read()
        if not ret:
            raise CameraReadError()
            
        output_frame = apply_filters(frame, effect_type)
        cv2.imshow("실시간 필터 적용", output_frame)
        
    except CameraReadError as e:
        logger.error(f"프레임 읽기 실패: {str(e)}")
        break
    except FilterApplyError as e:
        logger.error(f"필터 적용 실패: {str(e)}")
        continue
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {str(e)}")
        break

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
