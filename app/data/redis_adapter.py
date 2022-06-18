import redis


class RedisAdapter:
    def __init__(self) -> None:
        self.redis_client = redis.Redis(
            host='redis',
            port=6379,
            db=0,
            charset="utf-16",
            decode_responses=True
        )

    def get_data(self, text) -> str:
        return self.redis_client.get(text)

    def set_data(self, text, summary) -> None:
        self.redis_client.set(text, summary)
