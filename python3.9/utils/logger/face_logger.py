from .base_logger import BaseLogger

class FaceLogger(BaseLogger):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaceLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'logger'):
            super().__init__('face_detection', 'face_detection')
    
    @classmethod
    def get_logger(cls):
        return cls()