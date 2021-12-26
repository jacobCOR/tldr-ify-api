import os

import config
from app import create_app
from app.model.model_fetch import ModelCaller

model = ModelCaller()
env = os.getenv("ENVIRONMENT")
env = "production"
if env == "development":
    app = create_app(model, config_filename=config.DevelopmentConfig)
elif env == "production":
    app = create_app(model, config_filename=config.ProductionConfig)
else:
    app = create_app(model)

if __name__ == "__main__":
    if env == "production":
        from waitress import serve
        serve(app, host='0.0.0.0', port=8080)
    else:
        app.run()
