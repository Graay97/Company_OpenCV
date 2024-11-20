from exceptions import FilterInitError, FilterApplyError

filters = {}

def register_filter(effect_id):
    def decorator(func):
        filters[effect_id] = func
        return func
    return decorator

def apply_filter(filter_name, frame):
    try:
        if filter_name not in filters:
            raise FilterInitError(filter_name, "등록되지 않은 필터")
            
        return filters[filter_name](frame)
    except Exception as e:
        raise FilterApplyError(filter_name, str(e))