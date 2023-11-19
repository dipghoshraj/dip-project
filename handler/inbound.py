from model import redis_object, Phone_number





def inbound_ops(data):
    text, to, form, user_id = data.get('text', ''), data.get('to', None), data.get('form', None), data.get('user_id', None)

    phone_number = Phone_number.query.filter_by(number= to, account_id= user_id).first()
    if not phone_number:
        return {"message": "", "error": "to parameter not found"}, 400
    
    if 'stop' in text.lower():
        redis_object.set(f"calls:{str(form)}_{str(to)}", str(to), ex=3600*4)
    return {"message": "inbound sms ok","error": ""}, 200



