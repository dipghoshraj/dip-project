

from flask import request, jsonify
from model import Account, redis_object
from jsonschema import validate, ValidationError
import time

def authenticate_user(request):
    auth = request.authorization
    if not auth:
        return None

    username, password =  auth.username, auth.password
    user = Account.query.filter_by(auth_id = password, username = username).first()

    if user:
        return user
    return None


SCHEMA = {
    "type": "object",
    "properties": {
        "form": {"type": "string", "pattern": "^\d+$", "minLength": 6, "maxLength": 16},
        "to": {"type": "string", "pattern": "^\d+$", "minLength": 6, "maxLength": 16},
        "text": {"type": "string", "minLength": 1, "maxLength": 120},
    },
    "required": ["form", "to"]
}

RATE_LIMIT = 50
RATE_LIMIT_WINDOW = 24*3600  



def validdec(func):
    def wrapper(*args, **kwargs):
        try:
            data = request.get_json()
            print(data)
            text, to, form = data.get('text', ''), data.get('to', None), data.get('form', None)

            user = authenticate_user(request)
            if not user:
                return jsonify({'error': 'Unauthorized'}), 403

            for var_name, var_value in zip(['form', 'to', 'text'], [form, to, text]):
                 print(var_name, var_value)
                 if var_value is None:
                    return  jsonify({"message": "","error": f"{var_name} is missing"}), 400
                       
            validate(data, SCHEMA)
            data['user_id'] = user.id
            return func(data, *args, **kwargs)
        
        except ValidationError as e:
            print(e.path[0])
            return jsonify({'message': '', 'error': f'{e.path[0]} is invalid'}), 400
        except Exception as e:
            # raise
            return jsonify({'message': '', 'error': 'unknown error'}), 500
    wrapper.__name__ = func.__name__
    return wrapper


def api_call_limit(func):

    def check_limit(*args, **kwargs):
        try:
            data = request.get_json()
            text, to, form = data.get('text', ''), data.get('to', None), data.get('form', None)

            key = f"user:{form}"
            current_time = time.time()
            cutoff_time = current_time - RATE_LIMIT_WINDOW

            redis_object.zremrangebyscore(key, '-inf', cutoff_time)

            # Count the number of recent requests
            recent_requests = redis_object.zcount(key, cutoff_time, '+inf')

            print(recent_requests)
            if recent_requests < RATE_LIMIT:
                redis_object.zadd(key, {current_time: current_time})
                return func(*args, **kwargs)
            return jsonify({"message": "", "error": f"limit reached for from {form}"}), 400

        except Exception as e:
            return jsonify({'message': '', 'error': 'unknown error'}), 500
    return check_limit