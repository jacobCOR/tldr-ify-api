from pymongo import MongoClient


class MongoDBAdapter:
    def __init__(self):
        self.mongoDB = MongoClient(
            host="mongo_db_container",
            port=27017
        ).get_database('summarizations').get_collection('summary')

    def get_data(self, text):
        return self.mongoDB.find_one({"original": text})

    def set_data(self, text, summary, request):
        self.mongoDB.insert_one({"original": text,
                                 "summary": summary,
                                 "request_info": request})
