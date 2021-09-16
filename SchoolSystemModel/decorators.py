

def exception_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            print(err)
            return {'result': 'unexpected error'}, 500
    
    return wrapper