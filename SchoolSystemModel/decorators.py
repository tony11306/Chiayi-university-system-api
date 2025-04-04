

from flask.helpers import make_response
from flask import abort
from werkzeug.exceptions import BadRequest, ExpectationFailed, InternalServerError, Unauthorized
import logging

def exception_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Unauthorized:
            abort(401, {'result': 'account or password is is wrong'})
        except ExpectationFailed:
            abort(417, {'result': 'unable to connect to chayi university school system'})
        except BadRequest:
            abort(400, {'result': 'server can not understand the request.'})
        except Exception as err:
            logging.error(err)
            abort(500, {'result': 'unexpected error. It could be school system is under maintaining, or that page is unable to access currently.'})
    
    return wrapper