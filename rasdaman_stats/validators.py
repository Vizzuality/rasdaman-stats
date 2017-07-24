"""VALIDATORS"""
from functools import wraps
from rasdaman_stats.routes.api import error
from flask import request
import logging


def validate_geostore(func):
    """Validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("[Rasdamanstats Validator] Validating the presence of geostore")
        if 'geostoreId' in request.json:
            geostore = request.json['geostoreId']
        try:
            geostore
        except NameError:
            geostore = None
            return error(status=400, detail='Geostore needed')
        return func(*args, **kwargs)
    return wrapper
