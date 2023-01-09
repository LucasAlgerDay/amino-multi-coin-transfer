############################################################################################################
#                                     Helper Functions                                                     #
from os import environ
from binascii import unhexlify
from contextlib import suppress
from re import search
from typing import Callable
from requests import Response as HTTPResponse

def ggl(func):
    def wrapper(*args, **kwargs):
        args[0].gg += 1
        return func(*args, **kwargs)
    return wrapper

def check_debugger() -> bool:
    with suppress(Exception):
        return any([search("vsc", environ.get("TERM_PROGRAM")), search("pycharm", environ.get("TERM_PROGRAM"))])

def headers(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        xyz = func(*args, **kwargs)
        xyz[list(xyz.keys())[2]] = unhexlify(
            b"4170706c65206950686f6e6531332c3420694f53207631352e362e31204d61696e2f332e31322e39"
            ).decode("utf-8")
        return xyz
    return wrapper

def response(func: Callable):
    def wrapper(*args, **kwargs):
        response: HTTPResponse = func(*args, **kwargs)
        args[0].base_headers.update({"X-Request": response.headers.get("X-Response")})
        return response
    return wrapper

def request(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) if hasattr(args[0], unhexlify(b"6767").decode("utf-8")) else None
    return wrapper

############################################################################################################
