class CameraError(Exception):
    """카메라 관련 기본 예외 클래스"""
    pass

class CameraInitError(CameraError):
    """카메라 초기화 관련 예외"""
    def __init__(self, camera_id=0, message="카메라 초기화 실패"):
        self.camera_id = camera_id
        self.message = f"{message} (카메라 ID: {camera_id})"
        super().__init__(self.message)

class CameraReadError(CameraError):
    """카메라 프레임 읽기 관련 예외"""
    def __init__(self, message="프레임 읽기 실패"):
        self.message = message
        super().__init__(self.message)