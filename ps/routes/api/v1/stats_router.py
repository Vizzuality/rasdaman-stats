"""API ROUTER"""

import logging

from flask import jsonify, Blueprint
from ps.routes.api import error
from ps.validators import validate_greeting
from ps.middleware import set_something
from ps.serializers import serialize_greeting

psone_endpoints = Blueprint('psone_endpoints', __name__)


@psone_endpoints.route('/hello', strict_slashes=False, methods=['GET'])
@set_something
@validate_greeting
def say_hello(something):
    """World Endpoint"""
    logging.info('[ROUTER]: Say Hello')
    data = {
        'word': 'hello',
        'propertyTwo': 'random',
        'propertyThree': 'value',
        'something': something
    }
    if False:
        return error(status=400, detail='Not valid')
    return jsonify(data=[serialize_greeting(data)]), 200
