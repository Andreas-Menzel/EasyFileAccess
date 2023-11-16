from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask('.')
api = Api(app)

CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
