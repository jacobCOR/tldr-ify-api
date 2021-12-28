import logging.config
import os

import yaml

import config
from app import create_app
from app.model.model_fetch import ModelCaller


def init_logging():
    with open('./logging_conf.yml', 'r') as infile:
        configuration = yaml.safe_load(infile)
        logging.config.dictConfig(configuration)

    return logging.getLogger()


logger = init_logging()
model = ModelCaller(logger)

env = os.getenv("ENVIRONMENT")
if env == "development":
    app = create_app(model, logger, config_filename=config.DevelopmentConfig)
elif env == "production":
    app = create_app(model, logger, config_filename=config.ProductionConfig)
else:
    app = create_app(model, logger)

if __name__ == "__main__":
    if env == "production":
        from waitress import serve

        serve(app, host='0.0.0.0', port=8080)
    else:
        app.run(debug=True)
