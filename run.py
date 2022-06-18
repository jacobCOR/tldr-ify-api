import logging.config
import os

import yaml

import config
from app.celery.celery_utils import init_celery
from app.celery import celery

from app.main import create_app


def init_logging():
    with open('./logging_conf.yml', 'r') as infile:
        configuration = yaml.safe_load(infile)
        logging.config.dictConfig(configuration)

    return logging.getLogger()


if __name__ == "__main__":
    env = os.getenv("ENVIRONMENT")
    if env == "development":
        app = create_app(config_filename=config.DevelopmentConfig)
    elif env == "production":
        app = create_app(config_filename=config.ProductionConfig)
    else:
        app = create_app()

    init_celery(celery, app)

    if env == "production":
        from waitress import serve
        serve(app, host='0.0.0.0', port=8080)
    else:
        app.run(debug=True)
