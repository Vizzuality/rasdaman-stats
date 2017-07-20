"""API ROUTER"""

import numpy as np
import shapely
import picogeojson
import georasters as gr
from affine import Affine
from descartes import PolygonPatch
from rasterstats import zonal_stats
import fiona
import rasterio
from gdalconst import *
from osgeo import ogr
from io import BytesIO
import tempfile
import logging
import json
import copy
import gdal
from flask import jsonify, Blueprint, request
from rasdaman_stats.routes.api import error
from rasdaman_stats.validators import validate_request
# from rasdaman_stats.middleware import set_something
# from rasdaman_stats.serializers import serialize_greeting

from rasdaman_stats.services import query_service


rasdastats_endpoints = Blueprint('rasdastats_endpoints', __name__)

@rasdastats_endpoints.route('/stats/<dataset_id>', methods=['POST'])
def stats(dataset_id):
    """Queries the stats for a certain raster, with an optional mask"""
    logging.info('[StatsRouter] Obtaining stats for dataset_id: ' + dataset_id)
    logging.info("REQUEST")
    logging.info(request.json)

    dataset = {
        'datasetId': dataset_id
    }

    geostore = { 'geostoreId': request.json['geostoreId']} if request.json['geostoreId'] else {}

    
    options = {**dataset, **geostore}

    logging.info("Options: " + str(options))

    raster = query_service.get_raster(options)

    logging.info(raster)

    return "OK"
