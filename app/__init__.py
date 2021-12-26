import secrets
import string
import yaml
from os.path import exists

from flask import Flask
from flask_restful import Api

from .api.routes import api, Tldr
from .model.model_fetch import ModelCaller


def create_app(model, config_filename=None):
    app = Flask(__name__)
    app = secure_app(app)
    flask_api = Api(api)
    app.config['MODEL'] = model

    if config_filename:
        app.config.from_object(config_filename)

    with app.app_context():
        flask_api.add_resource(Tldr, '/v1/tldrify')
        app.register_blueprint(api, url_prefix="/app")

    return app


def create_secrets():
    print("creating secrets")
    yaml_api_key = {'api_key': ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(48))}
    print(yaml_api_key)
    with open('secrets.yml', 'w') as outfile:
        yaml.dump(yaml_api_key, outfile, default_style=False)


def load_secrets():
    with open('secrets.yml', 'r') as infile:
        try:
            return yaml.safe_load(infile)
        except yaml.YAMLError as exception:
            print(exception)


def secure_app(app):
    if not exists('secrets.yml'):
        create_secrets()
    app.config['secrets'] = load_secrets()
    return app
