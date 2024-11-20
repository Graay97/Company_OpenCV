class FilterError(Exception):
    """필터 관련 기본 예외 클래스"""
    pass

class FilterInitError(FilterError):
    """필터 초기화 관련 예외"""
    def __init__(self, filter_name, message="필터 초기화 실패"):
        self.filter_name = filter_name
        self.message = f"{message}: {filter_name}"
        super().__init__(self.message)

class FilterApplyError(FilterError):
    """필터 적용 관련 예외"""
    def __init__(self, filter_name, message="필터 적용 실패"):
        self.filter_name = filter_name
        self.message = f"{message}: {filter_name}"
        super().__init__(self.message)