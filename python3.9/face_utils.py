# face_utils.py

import dlib
import os
from logger import Logger

logger = Logger.get_face_logger()

def initialize_face_detectors(landmark_model_path='shape_predictor_68_face_landmarks.dat'):
    logger.info("얼굴 감지기 초기화 시작")
    
    try:
        logger.debug("프론트 페이스 디텍터 초기화 시도")
        detector = dlib.get_frontal_face_detector()
        logger.info("프론트 페이스 디텍터 초기화 성공")
        
        abs_path = os.path.abspath(landmark_model_path)
        logger.debug(f"랜드마크 파일 절대 경로: {abs_path}")
        logger.debug(f"파일 존재 여부: {os.path.exists(abs_path)}")
        
        if not os.path.exists(landmark_model_path):
            logger.error(f"랜드마크 파일을 찾을 수 없습니다: {landmark_model_path}")
            raise FileNotFoundError(f"랜드마크 파일을 찾을 수 없습니다: {landmark_model_path}")
        
        logger.debug("랜드마크 예측기 로드 시도")
        predictor = dlib.shape_predictor(landmark_model_path)
        logger.info("랜드마크 예측기 로드 성공")
        
        return detector, predictor
        
    except Exception as e:
        logger.error(f"얼굴 감지기 초기화 중 오류 발생: {str(e)}", exc_info=True)
        raise
