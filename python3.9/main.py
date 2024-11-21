# main.py
import cv2
import threading
from dataclasses import dataclass
from filters import filters
from filters.headband import headband_filter
from filters.three_d_effect import three_d_effect_filter
from utils import handle_key_input, initialize_face_detectors
from config import (
    EFFECT_NORMAL, EFFECT_HEADBAND,
    CAMERA_WIDTH, CAMERA_HEIGHT,
    VIDEO_FPS, VIDEO_CODEC,
    SCREENSHOTS_DIR, VIDEOS_DIR
)
from utils.logger import MainLogger, FaceLogger
from exceptions.camera_exceptions import CameraInitError, CameraReadError, FilterApplyError

# 로깅 설정
logger = MainLogger.get_logger()
face_logger = FaceLogger.get_logger()

logger.info("프로그램 시작")

# 얼굴 감지기 초기화
try:
    logger.debug("얼굴 감지기 초기화 시도")
    detector, predictor = initialize_face_detectors()
    face_detection_enabled = True
    logger.info("얼굴 감지기 초기화 성공")
except Exception as e:
    logger.error(f"얼굴 감지기 초기화 실패: {e}")
    detector, predictor = None, None
    face_detection_enabled = False

# 초기 설정
effect_type = EFFECT_NORMAL  # 기본 효과 설정
bRec = False                 # 녹화 상태 플래그
outputVideo = None           # VideoWriter 객체 초기화

# 카메라 초기화
try:
    cap = cv2.VideoCapture(0)  # 첫 번째 카메라 장치 사용
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    if not cap.isOpened():
        raise CameraInitError()
    logger.info("카메라 초기화 성공")
except Exception as e:
    logger.error(f"카메라 초기화 실패: {str(e)}")
    exit(1)

def apply_filters(frame, effect_type, flip=True):
    """
    선택된 효과를 프레임에 적용하는 함수

    Args:
        frame (numpy.ndarray): 입력 프레임
        effect_type (int): 적용할 효과의 타입
        flip (bool): 프레임을 좌우 반전할지 여부

    Returns:
        numpy.ndarray: 필터가 적용된 프레임
    """
    try:
        # 프레임 좌우 반전
        if flip:
            frame = cv2.flip(frame, 1)
        
        # 헤드밴드 효과 적용
        if effect_type == EFFECT_HEADBAND:
            if not face_detection_enabled:
                logger.warning("얼굴 감지 기능을 사용할 수 없습니다")
                return frame
            
            # 회색조 변환
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            logger.debug("얼굴 감지 시도")
            faces = detector(gray)
            logger.debug(f"감지된 얼굴 수: {len(faces)}")
            
            # 감지된 각 얼굴에 헤드밴드 필터 적용
            if len(faces) > 0:
                for face in faces:
                    frame = headband_filter(frame, predictor, face, gray)
            return frame

        # 기타 효과 적용
        return filters.get(effect_type, lambda x: x)(frame)
    except UnboundLocalError as e:
        logger.error(f"UnboundLocalError 발생: {e}", exc_info=True)
        return frame
    except Exception as e:
        logger.error(f"필터 적용 중 오류 발생: {e}", exc_info=True)
        return frame

def process_frame(frame, effect_type, result_container):
    """
    스레드에서 프레임 처리하는 함수

    Args:
        frame (numpy.ndarray): 입력 프레임
        effect_type (int): 적용할 효과의 타입
        result_container (dict): 결과 프레임을 저장할 컨테이너
    """
    result_container['output_frame'] = apply_filters(frame, effect_type)

while True:
    try:
        # 프레임 캡처
        ret, frame = cap.read()
        if not ret:
            raise CameraReadError()
        
        # 필터 적용을 위한 스레드 시작
        result_container = {}
        filter_thread = threading.Thread(target=process_frame, args=(frame, effect_type, result_container))
        filter_thread.start()
        filter_thread.join()
        
        output_frame = result_container.get('output_frame', frame)
        cv2.imshow("실시간 필터 적용", output_frame)  # 필터 적용된 프레임 표시

    except CameraReadError as e:
        logger.error(f"프레임 읽기 실패: {str(e)}")
        break
    except FilterApplyError as e:
        logger.error(f"필터 적용 실패: {str(e)}")
        continue
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {str(e)}")
        break

    # 키 입력 처리
    key = cv2.waitKey(1) & 0xFF
    if key != 255:
        result = handle_key_input(key, effect_type, bRec, outputVideo, output_frame)
        
        if result.exit_signal:
            logger.info("종료 신호 수신")
            print("종료합니다.")
            break
        
        # 효과 타입 및 녹화 상태 업데이트
        effect_type, bRec, outputVideo = result.effect_type, result.bRec, result.outputVideo

    # 녹화 중이라면 프레임을 비디오 파일에 기록
    if bRec and outputVideo is not None:
        outputVideo.write(output_frame)

# 종료 전 정리 작업
cv2.waitKey(1)
cap.release()  # 카메라 해제
if outputVideo is not None:
    outputVideo.release()
cv2.destroyAllWindows()  # 모든 OpenCV 윈도우 닫기
cv2.waitKey(1)
logger.info("프로그램 종료")
