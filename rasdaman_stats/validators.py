"""VALIDATORS"""

from functools import wraps

from rasdaman_stats.routes.api import error


def validate_request(func):
    """Validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if False:
            return error(status=400, detail='Validating something in the middleware')
        return func(*args, **kwargs)
    return wrapper
