import logging

import src.app_data as app_data
from src.flaskr.app import app, api
from src.flaskr.endpoints.files import EPFiles

logging.basicConfig(level=logging.DEBUG)
logging.debug(app_data.conf)


@app.route('/')
def index():
    return 'Hello World!'


api.add_resource(EPFiles, '/files/<string:file_path>')
