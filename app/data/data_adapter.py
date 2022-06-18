from app.data.mongoDB_adapter import MongoDBAdapter
from app.data.redis_adapter import RedisAdapter

from app.model.model_fetch import ModelCaller
from app.celery import celery


class DataAdapter:
    def __init__(self):
        self.mongo_adapter = MongoDBAdapter()
        self.redis_adapter = RedisAdapter()
        self.model_caller = ModelCaller()

    def get_data(self, text_to_summarize, request) -> (str, str):
        # should fetch from Redis if miss -> Mongo if miss -> Query Model

        summary = self.redis_adapter.get_data(text_to_summarize)
        if not summary:
            summary = self.mongo_adapter.get_data(text_to_summarize)
            self.__populate_redis(text_to_summarize, summary)
        if not summary:
            summary = self.model_caller.model_call(text_to_summarize)
            self.__populate_redis(text_to_summarize, summary)
        # TODO make this celery viable https://docs.celeryq.dev/en/stable/userguide/calling.html
        self.__populate_mongo(text_to_summarize, summary, request)
        return text_to_summarize, summary

    def __populate_redis(self, text_to_summarize, summary):
        self.redis_adapter.set_data(text_to_summarize, summary)

    def __populate_mongo(self, text_to_summarize, summary, request):
        self.mongo_adapter.set_data(text_to_summarize, summary, dict(request))
