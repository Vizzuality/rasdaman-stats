import json
import jsonpath
import os
from requests import Request, Session
import logging
from rasdaman_stats.errors import Error
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

    logging.info('[QueryService] Getting mask from geostore')
    vector_mask = get_geostore(config)
    logging.debug(vector_mask)

    bbox = vector_mask["data"]["attributes"]["bbox"]
    logging.debug("BBOX: " + ', '.join(str(coord) for coord in bbox))

    fields = get_fields(config)
    coverage_name = fields["coverageId"]

    extra_axes_dct = config.get('additionalAxes')
    extra_axes_str_arr = []
    if extra_axes_dct:
        for axis, datum in extra_axes_dct.items():
            extra_axes_str_arr.append( "".join([",", str(axis), "(\"", str(datum), "\")"]))
            extra_axes_str = "".join(extra_axes_str_arr)
    else:
        extra_axes_str = ""

    # Only slicing - not subsetting
    logging.info(str(extra_axes_str))

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
    logging.debug("WCPS: " + wcps_query)

    logging.info('[QueryService] Getting raster from rasdaman')
    # Need to update the CT plugin to allow raw responses

    request_url = CT_URL + '/' + API_VERSION + '/query/' + config.get('datasetId')
    session = Session()

    request = Request(
        method = "POST",
        url = request_url,
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + CT_TOKEN
        },
        data = json.dumps({"wcps": wcps_query})
    )

    prepped = session.prepare_request(request)
    response = session.send(prepped)



    
    with tempfile.NamedTemporaryFile(suffix='.tiff', delete=False) as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
        # dataset = gdal.Open(f.name)
    with tempfile.NamedTemporaryFile(suffix='.geo.json', delete=False) as g:
        logging.debug("GEOJSON")
        encoded_data = json.dumps(vector_mask["data"]["attributes"]["geojson"])
        logging.debug(encoded_data)
        g.write(encoded_data.encode())
        g.close()
        logging.info("Files: " + f.name + " " + g.name)
        stats = zonal_stats(g.name, f.name, all_touched=True)
    logging.info("STATS")
    logging.info(stats)
    return stats

def get_geostore(config):
    logging.info('[QueryService] Getting geostore')
    try:
        request_options = {
            'uri': '/geostore/' + config.get('geostore'),
            'method': 'GET'
        }
        response = request_to_microservice(request_options)
    except Exception as error:
        raise error
    return response

def get_fields(config):
    logging.info('[QueryService] Getting fields for dataset')
    try:
        request_options = {
            'uri': '/fields/' + config.get('datasetId'),
            'method': 'GET'
        }
        response = request_to_microservice(request_options)
    except Exception as error:
        raise error
    return response
