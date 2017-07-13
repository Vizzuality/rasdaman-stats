"""API ROUTER"""

import logging
import json
import copy
from flask import jsonify, Blueprint
from rasdaman_stats.routes.api import error
from rasdaman_stats.validators import validate_request
# from rasdaman_stats.middleware import set_something
from rasdaman_stats.serializers import serialize_greeting

rasdastats_endpoints = Blueprint('rasdastats_endpoints', __name__)

# @rasdastats_endpoints.route('/hello', strict_slashes=False, methods=['GET'])
# @validate_request
# def say_hello(something):
#     """World Endpoint"""
#     logging.info('[ROUTER]: Say Hello')
#     data = {
#         'word': 'hello',
#         'propertyTwo': 'random',
#         'propertyThree': 'value',
#         'something': something
#     }
#     if False:
#         return error(status=400, detail='Not valid')
#     return jsonify(data=[serialize_greeting(data)]), 200


@rasdastats_endpoints.route('/stats/<dataset_id>', methods=['POST'])
def stats(dataset_id):
    """Queries the stats for a certain raster, with an optional mask"""
    logging.info(str.join('Obtaining stats for dataset_id', dataset_id))
    return None
