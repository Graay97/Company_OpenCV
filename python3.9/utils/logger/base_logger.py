import logging
import os
from datetime import datetime

class BaseLogger:
    def __init__(self, logger_name, log_file_prefix):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        
        # 로그 디렉토리 생성
        self.log_dir = 'logs'
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        # 로그 파일명 설정
        current_date = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(self.log_dir, f'{log_file_prefix}_{current_date}.log')
        
        # 파일 핸들러 설정
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 콘솔 핸들러 설정
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 포맷터 설정
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 핸들러 추가
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message, exc_info=True):
        self.logger.error(message, exc_info=exc_info)