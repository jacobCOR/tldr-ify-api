import os


class BaseConfig(object):
    DEBUG = False
    MONGO_URI = "mongo_uri"


class DevelopmentConfig(BaseConfig):
    DEBUG = False
    ENV = "development"
    MONGO_URI = os.getenv("MONGODB_CONNSTRING")


class TestingConfig(BaseConfig):
    DEBUG = True
    MONGO_URI = "testing_mongo_uri"


class ProductionConfig(BaseConfig):
    MONGO_URI = "production_mongo_uri"
    FLASK_ENV = "production"
