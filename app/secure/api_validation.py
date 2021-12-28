
from flask import request, abort
from flask import current_app as app


def match_api_keys(key):
    if key is None:
        return False
    api_key = app.config['secrets']
    if api_key is None:
        return False
    elif api_key['api_key'] == key:
        return True
    return False


def require_key(f):
    def wrapper(*args, **kwargs):
        if match_api_keys(request.args.get('key')):
            return f(*args, **kwargs)
        else:
            app.config['LOGGER'].warning("Unauthorized access trying to use API: " + request.remote_addr)
            abort(401)
    return wrapper
