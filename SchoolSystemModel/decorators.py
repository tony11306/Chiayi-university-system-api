

from flask_restful import abort


def exception_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            print(err)
            abort(500, {'result': 'unexpected error'})
    
    return wrapper