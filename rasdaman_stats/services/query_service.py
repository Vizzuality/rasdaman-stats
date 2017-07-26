import json
import jsonpath
import os
from requests import Request, Session
import logging
from rasdaman_stats.errors import Error, GeostoreNotFound
import tempfile
from rasterstats import zonal_stats
from osgeo import gdal
from gdalconst import *
from CTRegisterMicroserviceFlask import request_to_microservice

CT_URL = os.getenv('CT_URL')
CT_TOKEN = os.getenv('CT_TOKEN')
API_VERSION = os.getenv('API_VERSION')

def get_stats(config):
    # TODO: errors
    logging.info('[QueryService] Obtaining statistics')
    
    dataset = config.get('datasetId')
    logging.info('[QueryService] Getting mask from geostore')
    vector_mask = get_geostore(config.get('geostore'))
    bbox = vector_mask["data"]["attributes"]["bbox"]

    logging.debug('[QueryService] Getting fields from dataset')
    fields = get_fields(dataset) 
    coverage_name = fields["coverageId"]

    # If there are any additional axes present:
    extra_axes_dct = config.get('additionalAxes')
    extra_axes_str_arr = []
    extra_axes_str = ""
    if extra_axes_dct:
        for axis, datum in extra_axes_dct.items():
            extra_axes_str_arr.append( "".join([",", str(axis), "(\"", str(datum), "\")"]))
            extra_axes_str = "".join(extra_axes_str_arr)

    # Building the query
    query_array = [
        "for cov in (",
        coverage_name,
        ") return encode( cov[",
        "Long(",
        ":".join([str(bbox[0]), str(bbox[2])]),
        "), Lat(",
        ":".join([str(bbox[1]), str(bbox[3])]),
        ")",
        extra_axes_str,
        "], \"GTiff\")"
    ]
    wcps_query = ''.join(query_array)

    
    rasterFile  = get_raster_file(dataset, wcps_query)
    vectorFile = get_vector_file(vector_mask)
    
    stats = zonal_stats(vectorFile, rasterFile, all_touched=True)
    os.remove(os.path.join('/tmp', rasterFile))
    os.remove(os.path.join('/tmp', vectorFile))
    return stats

def get_vector_file(vector_mask):
    with tempfile.NamedTemporaryFile(suffix='.geo.json', delete=False) as f:
        vector_filename = f.name
        encoded_data = json.dumps(vector_mask["data"]["attributes"]["geojson"])
        f.write(encoded_data.encode())
        f.close()
    return vector_filename

def get_raster_file(dataset, query):
    logging.info('[QueryService] Getting raster from rasdaman')
    # Need to update the CT plugin to allow raw responses
    request_url = CT_URL + '/' + API_VERSION + '/query/' + dataset
    session = Session()
    request = Request(
        method = "POST",
        url = request_url,
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + CT_TOKEN
        },
        data = json.dumps({"wcps": query})
    )
    prepped = session.prepare_request(request)
    response = session.send(prepped)
    with tempfile.NamedTemporaryFile(suffix='.tiff', delete=False) as f:
        for chunk in response.iter_content(chunk_size=1024):
            raster_filename = f.name
            f.write(chunk)
        f.close()
    return raster_filename

def get_geostore(geostore):
    logging.info('[QueryService] Getting geostore')
    try:
        request_options = {
            'uri': '/geostore/' + geostore,
            'method': 'GET'
        }
        response = request_to_microservice(request_options)
        if 'errors' in response:
            raise GeostoreNotFound(message='Error obtaining geostore')
        logging.debug('GEOSTORE RESPONSE: ' + str(response))
    except Exception as error:
        logging.error(str(error))
        raise GeostoreNotFound(message='Error obtaining geostore')
    return response

def get_fields(dataset):
    logging.info('[QueryService] Getting fields for dataset')
    try:
        request_options = {
            'uri': '/fields/' + dataset,
            'method': 'GET'
        }
        response = request_to_microservice(request_options)
    except Exception as error:
        raise error
    return response
