from flask import Blueprint, request, Response
from flask_restful import Resource
from flask import current_app as app

from app.secure.api_validation import require_key

api = Blueprint('api', __name__)


def verify_json(json_data):
    if len(json_data) <= 0:
        return False
    elif len(json_data) > 10000:
        return False
    else:
        return True


class Tldr(Resource):
    @staticmethod
    @require_key
    def get():
        json_data = request.get_json()
        valid_json = verify_json(json_data['text'])
        if not json_data or not valid_json:
            return Response("Invalid JSON format",
                            status=400)

        original, summary = app.config['MODEL'].model_call(json_data['text'])
        return {'text': original,
                'summary': summary}
