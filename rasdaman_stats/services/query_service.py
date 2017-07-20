import json
import jsonpath
import os
from requests import Request, Session
import logging
from rasdaman_stats.errors import Error


from CTRegisterMicroserviceFlask import request_to_microservice

CT_URL = os.getenv('CT_URL')
CT_TOKEN = os.getenv('CT_TOKEN')
API_VERSION = os.getenv('API_VERSION')

def get_stats(config):
    # TODO: errors
    logging.info('[QueryService] Obtaining statistics')

    request_url = CT_URL + '/' + API_VERSION + '/query/' + config.get('datasetId')
    session = Session()

    logging.info('[QueryService] Getting mask from geostore')
    vector_mask = get_geostore(config)
    logging.info(vector_mask)

    bbox = vector_mask["data"]["attributes"]["bbox"]
    logging.info("BBOX: " + ', '.join(str(coord) for coord in bbox))
    
    logging.info('[QueryService] Getting raster from rasdaman')
    # Need to update the CT plugin to allow raw responses

    fields = get_fields(config)
    coverage_name = fields["coverageId"]
    logging.info(coverage_name)

    query_array = [
        "for cov in (",
        coverage_name,
        ") return encode( cov[",
        "Long(",
        ":".join([str(bbox[0]), str(bbox[2])]),
        "), Lat(",
        ":".join([str(bbox[1]), str(bbox[3])]),
        ")], \"GTiff\")"
    ]

    wcps_query = ''.join(query_array)
    logging.debug("WCPS: " + wcps_query)

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
    return response.content

def get_geostore(config):
    logging.info('[QueryService] Getting geostore')
    try:
        request_options = {
            'uri': '/geostore/' + config.get('geostoreId'),
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
