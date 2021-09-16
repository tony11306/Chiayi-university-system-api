import requests
import json

from requests.api import head

def decorator(func):
    def wrapper(*args, **kwargs):
        print('fizz')
        func(*args, **kwargs)
    return wrapper
class Fizz:

    def __init__(self) -> None:
        pass
    
    @decorator
    def buzz(self, name, ww):
        print('buzz', name, ww)


fizz = Fizz()
fizz.buzz('hello', 'ww')