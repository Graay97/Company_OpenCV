# main.py
import cv2
import threading
from dataclasses import dataclass
from filters import filters
from filters.headband import headband_filter
from utils import handle_key_input, initialize_face_detectors
from config import (
    EFFECT_NORMAL, EFFECT_HEADBAND, EFFECT_CARTOONIFY,
    EFFECT_VINTAGE, EFFECT_BEAUTY,
    CAMERA_WIDTH, CAMERA_HEIGHT,
    VIDEO_FPS, VIDEO_CODEC,
    SCREENSHOTS_DIR, VIDEOS_DIR
)
from utils.logger import MainLogger, FaceLogger
from exceptions.camera_exceptions import CameraInitError, CameraReadError, FilterApplyError
import dlib
import platform
from concurrent.futures import ThreadPoolExecutor

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
    # 백엔드 선택 최적화
    if platform.system() == 'Windows':
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    
    # 필수 설정만 먼저 적용
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    # 빠른 초기화를 위한 설정
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))  # MJPG 포맷 사용
    cap.set(cv2.CAP_PROP_FPS, 30)  # 기본 FPS
    
    # 불필요한 자동 설정 비활성화
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # 자동 노출 비활성화
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # 자동 초점 비활성화
    
    # 빠른 워밍업
    for _ in range(3):  # 5회에서 3회로 감소
        cap.grab()
    
    if not cap.isOpened():
        raise CameraInitError()
    logger.info("카메라 초기화 성공")

except Exception as e:
    logger.error(f"카메라 초기화 실패: {str(e)}")
    exit(1)

@dataclass
class FaceDetectionCache:
    frame_count: int = 0
    last_faces = None
    last_gray = None
    SKIP_FRAMES = 2  # 몇 프레임마다 얼굴 감지를 할지 설정

# 역 변수로 캐시 객체 생성
face_cache = FaceDetectionCache()

# 필터 이름 딕셔너리 수정
FILTER_NAMES = {
    EFFECT_NORMAL: u"기본 화면",
    EFFECT_CARTOONIFY: u"카툰 필터",
    EFFECT_VINTAGE: u"빈티지 필터",
    EFFECT_HEADBAND: u"머리띠 필터",
    EFFECT_BEAUTY: u"뷰티 필터",
}

def add_filter_name(frame, effect_type):
    """프레임에 현재 필터 이름을 추가하는 함수"""
    filter_name = FILTER_NAMES.get(effect_type, u"알 수 없는 필터")
    
    # OpenCV에서 한글 표시를 위한 설정
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    
    # PIL 이미지로 변환
    pil_img = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_img)
    
    # 폰트 설정 (시스템에 설치된 한글 폰트 경로 지정)
    try:
        font = ImageFont.truetype("malgun.ttf", 20)  # Windows의 경우
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", 20)  # Linux의 경우
        except:
            return frame  # 폰트를 찾을 수 없는 경우 원본 프레임 반환
    
    # 텍스트 그리기
    text = f"현재 필터: {filter_name}"
    draw.text((20, 20), text, font=font, fill=(255, 255, 255))
    
    # 키 가이드 추가
    guide_text = u"0: 기본 / 1: 카툰 / 2: 빈티지 / 3: 머리띠 / 4: 뷰티 / Q: 종료"
    draw.text((20, frame.shape[0] - 40), guide_text, font=font, fill=(255, 255, 255))
    
    # numpy 배열로 다시 변환
    return np.array(pil_img)

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
            
            # 프레임 크기 축소
            scale = 0.5
            small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            
            # 캐시된 얼굴 위치 사용
            if face_cache.frame_count % face_cache.SKIP_FRAMES == 0:
                logger.debug("얼굴 감지 시도")
                faces = detector(gray)
                face_cache.last_faces = faces
                face_cache.last_gray = gray
            else:
                faces = face_cache.last_faces
                gray = face_cache.last_gray
            
            face_cache.frame_count += 1
            
            if faces and len(faces) > 0:
                for face in faces:
                    # 축소된 이미지에서의 얼굴 위치를 원본 크기로 조정
                    scaled_face = scale_rect(face, 1/scale)
                    frame = headband_filter(frame, predictor, scaled_face, cv2.resize(gray, (frame.shape[1], frame.shape[0])))
            return frame

        # 기타 효과 적용
        return filters.get(effect_type, lambda x: x)(frame)
    except Exception as e:
        logger.error(f"필터 적용 중 오류 발생: {e}", exc_info=True)
        return frame

def scale_rect(rect, scale):
    """dlib의 rectangle 객체의 크기를 조정하는 헬퍼 함수"""
    new_left = int(rect.left() * scale)
    new_top = int(rect.top() * scale)
    new_right = int(rect.right() * scale)
    new_bottom = int(rect.bottom() * scale)
    return dlib.rectangle(new_left, new_top, new_right, new_bottom)

def process_frame(frame, effect_type, result_container):
    """스레드에서 프레임 처리하는 함수"""
    try:
        filtered_frame = apply_filters(frame, effect_type)
        filtered_frame = add_filter_name(filtered_frame, effect_type)
        result_container['output_frame'] = filtered_frame
    except Exception as e:
        logger.error(f"프레임 처리 실패: {str(e)}")
        result_container['output_frame'] = frame

# 프레임 처리를 위한 스레드 풀 생성
thread_pool = ThreadPoolExecutor(max_workers=2)

while True:
    try:
        # 프레임 캡처 최적화
        if not cap.grab():  # 먼저 프레임을 가져오고
            raise CameraReadError()
        ret, frame = cap.retrieve()  # 필요할 때 디코딩
        
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
