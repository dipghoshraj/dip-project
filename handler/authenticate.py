

from flask import request, jsonify
from model import Account
from jsonschema import validate, ValidationError

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
        "form": {"type": "string", "minLength": 6, "maxLength": 16},
        "to": {"type": "string", "minLength": 6, "maxLength": 16},
        "text": {"type": "string", "minLength": 1, "maxLength": 120},
    },
    "required": ["form", "to"]
}



def validdec(func):
    def wrapper(*args, **kwargs):
        try:
            data = request.get_json()
            text, to, form = data.get('text', ''), data.get('to', None), data.get('form', None)

            user = authenticate_user(request)
            if not user:
                return jsonify({'error': 'Unauthorized'}), 403

            for var_name, var_value in zip(['form', 'to', 'text'], [text, to, form]):
                 if var_value is None:
                    return  jsonify({"message": "","error": f"{var_name} is missing"})
                 
           
            
            validate(data, SCHEMA)
            data['user_id'] = user.id
            return func(data, *args, **kwargs)
        
        except ValidationError as e:
            print(e.path[0])
            return jsonify({'message': '', 'error': f'{e.path[0]} is invalid'}), 400
        except Exception as e:
            return jsonify({'message': '', 'error': 'unknown error'}), 500
    wrapper.__name__ = func.__name__
    return wrapper