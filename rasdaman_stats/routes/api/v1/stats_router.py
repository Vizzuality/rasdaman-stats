"""API ROUTER"""
import logging
import json
from flask import jsonify, Blueprint, request
from rasdaman_stats.routes.api import error
from rasdaman_stats.errors import Error, GeostoreNotFoundError
from rasdaman_stats.validators import validate_geostore
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
            'geostore': request.json['geostore']
    } if request.json['geostore'] else {'geostore': None}
        
    additional_axes = {
        'additionalAxes': request.json['additionalAxes']
    } if 'additionalAxes' in request.json else {
        'additionalAxes': None
    }
    
    options = {**dataset, **geostore, **additional_axes}    
    logging.info("Options: " + str(options))
    try:
        stats = query_service.get_stats(options)
    except GeostoreNotFoundError:
        return error(status=404, detail="Geostore not found")
    return json.dumps({"data": stats})
