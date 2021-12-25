import os

import config
from app import create_app
from app.model.model_fetch import ModelCaller

model = ModelCaller()
if os.getenv("ENVIRONMENT") == "development":
    app = create_app(model, config_filename=config.DevelopmentConfig)
else:
    app = create_app(model)

if __name__ == "__main__":

    app.run(host='0.0.0.0')
