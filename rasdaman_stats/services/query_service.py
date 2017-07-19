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

def get_raster(config):
    # TODO: errors
    logging.info('[QueryService] Getting raster from rasdaman')

    session = Session()

    request_url = CT_URL + '/' + API_VERSION + '/query/' + config.get('datasetId')

    vector_mask = get_geostore(config)
    bbox = vector_mask["data"]["attributes"]["bbox"]
    logging.info("BBOX: " + ', '.join(str(coord) for coord in bbox))
    

    logging.info('[QueryService] Getting raster from rasdaman')
    logging.info(vector_mask)

    
    
    request = Request(
        method = "POST",
        url = request_url,
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + CT_TOKEN
        },
        data = json.dumps(config.get('body'))
    )

    prepped = session.prepare_request(request)
    response = session.send(prepped)
    return response.content

def get_geostore(config):
    logging.info('[QueryService] Getting geostore with config')
    logging.info(config)
    try:
        request_options = {
            'uri': '/geostore/' + config.get('geostoreId'),
            'method': 'GET'
        }
        response = request_to_microservice(request_options)
        
    except Exception as error:
        raise error

    return response

    
    
    
