

from flask.helpers import make_response
from flask_restful import abort


def exception_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            print(err)
            abort(make_response(500, result='unexpected error'))
    
    return wrapper