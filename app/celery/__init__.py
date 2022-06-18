from celery import Celery


def make_celery(app_name=__name__) -> Celery:
    redis_uri_broker = "redis://redis:6379/0"
    redis_url_backend = "redis://redis:6379/1"
    return Celery(app_name, broker=redis_uri_broker, backend=redis_url_backend)


celery = make_celery()
