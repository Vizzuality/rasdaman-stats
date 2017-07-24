"""API ROUTER"""

import rasterio
import logging
import json
import copy
from flask import jsonify, Blueprint, request
from rasdaman_stats.routes.api import error
from rasdaman_stats.validators import validate_geostore
# from rasdaman_stats.middleware import set_something
# from rasdaman_stats.serializers import serialize_greeting

from rasdaman_stats.services import query_service

rasdastats_endpoints = Blueprint('rasdastats_endpoints', __name__)

@rasdastats_endpoints.route('/stats/<dataset_id>', methods=['POST'])
@validate_geostore
def stats(dataset_id):
    """Queries the stats for a certain raster, with an optional mask"""
    logging.info('[StatsRouter] Obtaining stats for dataset_id: ' + dataset_id)
    logging.info("REQUEST")
    logging.info(request.json)
    
    dataset = {
        'datasetId': dataset_id
    }

    geostore = {
        'geostoreId': request.json['geostoreId']
    } if request.json['geostoreId'] else {}

    additional_axes = {
        'additionalAxes': request.json['additionalAxes']
    } if request.json['additionalAxes'] else {}
    
    options = {**dataset, **geostore, **additional_axes}

    
    logging.info("Options: " + str(options))

    stats = query_service.get_stats(options)

    return json.dumps({"data": stats})
