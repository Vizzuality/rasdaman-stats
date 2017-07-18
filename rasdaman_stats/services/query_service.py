import json
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
    request = Request(
        method = "POST",
        url = CT_URL + '/' + API_VERSION + '/query/' + config.get('dataset_id'),
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + CT_TOKEN
        },
        data = json.dumps(config.get('body'))
    )

    prepped = session.prepare_request(request)
    response = session.send(prepped)
    return response.raw
