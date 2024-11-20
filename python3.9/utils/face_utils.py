# face_utils.py

import dlib
import os
from utils.logger import FaceLogger

logger = FaceLogger.get_logger()

def initialize_face_detectors():
    logger.info("얼굴 감지기 초기화 시작")
    
    try:
        logger.debug("프론트 페이스 디텍터 초기화 시도")
        detector = dlib.get_frontal_face_detector()
        logger.info("프론트 페이스 디텍터 초기화 성공")
        
        # 현재 파일의 절대 경로를 기준으로 landmark 파일 경로 설정
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        landmark_model_path = os.path.join(current_dir, 'shape_predictor_68_face_landmarks.dat')
        
        # 디버그를 위한 경로 출력
        logger.debug(f"랜드마크 파일 절대 경로: {landmark_model_path}")
        logger.debug(f"파일 존재 여부: {os.path.exists(landmark_model_path)}")
        
        if not os.path.exists(landmark_model_path):
            logger.error(f"랜드마크 파일을 찾을 수 없습니다: {landmark_model_path}")
            raise FileNotFoundError(f"랜드마크 파일을 찾을 수 없습니다: {landmark_model_path}")
        
        logger.debug("랜드마크 예측기 로드 시도")
        predictor = dlib.shape_predictor(landmark_model_path)
        logger.info("랜드마크 예측기 로드 성공")
        
        return detector, predictor
        
    except Exception as e:
        logger.error(f"얼굴 감지기 초기화 중 오류 발생: {str(e)}")
        raise
