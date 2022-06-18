from flask import Blueprint, request, Response, abort
from flask_restful import Resource

from flask import current_app as app
from app.secure.api_validation import require_key

api = Blueprint('api', __name__)


def verify_json(json_data) -> bool:
    """
    checks json length
    :param json_data:
    :return: bool
    """
    if len(json_data) <= 0:
        return False
    elif len(json_data) > 100000:
        return False
    else:
        return True


def is_valid_json(json_data):
    # TODO check if this contains a text field
    if not json_data:
        abort(Response("No JSON in request",
                       status=400))
    valid_json = verify_json(json_data['text'])
    if not valid_json:
        abort(Response("Invalid JSON format",
                       status=400))


class Tldr(Resource):
    @staticmethod
    @require_key
    def post():
        json_data = request.get_json()
        is_valid_json(json_data)
        text_to_summarize = json_data['text']
        data_adapter = app.config['DATA']
        original, summary = data_adapter.get_data(text_to_summarize, request.headers)
        return {'text': original,
                'summary': summary}
