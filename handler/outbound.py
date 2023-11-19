from model import redis_object, Phone_number
import time



RATE_LIMIT = 50  # Adjust the rate limit as needed
RATE_LIMIT_WINDOW = 60  # Adjust the rate limit window in seconds

def outbound_ops(data):
    text, to, form, user_id = data.get('text', ''), data.get('to', None), data.get('form', None), data.get('user_id', None)

    key = f"calls:{str(to)}_{str(form)}"
    data = redis_object.get(key)
    if data:
        return {"message": "", "error": f"sms from {form} to {to} blocked by STOP request"}, 400
    
    phone_number = Phone_number.query.filter_by(number= form, account_id= user_id).first()
    if not phone_number:
        return {"message": "", "error": "from parameter not found"}, 400
    return {"message": "outbound sms ok","error": ""}, 200

