import logging
import os
from datetime import datetime

class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            # 로그 디렉토리 생성
            self.log_dir = 'logs'
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

            # 로그 파일명에 날짜 추가
            current_date = datetime.now().strftime('%Y%m%d')
            self.log_file = os.path.join(self.log_dir, f'application_{current_date}.log')
            self.face_detection_log = os.path.join(self.log_dir, f'face_detection_{current_date}.log')

            # 메인 로거 설정
            self.logger = logging.getLogger('main')
            self.logger.setLevel(logging.DEBUG)

            # 얼굴 인식 로거 설정
            self.face_logger = logging.getLogger('face_detection')
            self.face_logger.setLevel(logging.DEBUG)

            # 포맷터 설정
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

            # 메인 로거 핸들러
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # 얼굴 인식 로거 핸들러
            face_file_handler = logging.FileHandler(self.face_detection_log, encoding='utf-8')
            face_file_handler.setFormatter(formatter)
            self.face_logger.addHandler(face_file_handler)
            self.face_logger.addHandler(console_handler)

            Logger._initialized = True

    @classmethod
    def get_main_logger(cls):
        if cls._instance is None:
            cls()
        return cls._instance.logger

    @classmethod
    def get_face_logger(cls):
        if cls._instance is None:
            cls()
        return cls._instance.face_logger