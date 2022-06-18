import secrets
import string
from os.path import exists

import yaml
from flask import Flask
from flask import current_app
from flask_restful import Api

from app.api.routes import Tldr, api
from app.data.data_adapter import DataAdapter


def create_app(config_filename=None):
    app = Flask(__name__)
    app = secure_app(app)
    flask_api = Api(api)
    app.config['DATA'] = DataAdapter()

    if config_filename:
        app.config.from_object(config_filename)

    with app.app_context():
        flask_api.add_resource(Tldr, '/v1/tldrify')
        app.register_blueprint(api, url_prefix="/app")

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app


def create_secrets():
    current_app.config['LOGGER'].info("Generating Secrets.yml")
    yaml_api_key = {'api_key': ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(48))}
    current_app.config['LOGGER'].info(yaml_api_key)
    with open('secrets.yml', 'w') as outfile:
        yaml.dump(yaml_api_key, outfile, default_style=False)


def load_secrets():
    with open('secrets.yml', 'r') as infile:
        try:
            return yaml.safe_load(infile)
        except yaml.YAMLError as exception:
            current_app.config['LOGGER'].error(exception)


def secure_app(app):
    if not exists('secrets.yml'):
        create_secrets()
    app.config['secrets'] = load_secrets()
    return app
