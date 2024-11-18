# face_utils.py

import dlib
import os

def initialize_face_detectors(landmark_model_path='shape_predictor_68_face_landmarks.dat'):
    # 얼굴 탐지기 초기화
    detector = dlib.get_frontal_face_detector()
    
    # 랜드마크 예측기 로드
    if not os.path.exists(landmark_model_path):
        print(f"랜드마크 파일을 찾을 수 없습니다. {landmark_model_path} 경로를 확인하세요.")
        predictor = None
    else:
        try:
            predictor = dlib.shape_predictor(landmark_model_path)
        except dlib.error as e:
            print(f"랜드마크 예측기 로드 실패: {str(e)}")
            predictor = None

    return detector, predictor
