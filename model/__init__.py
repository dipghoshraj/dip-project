from flask_sqlalchemy import SQLAlchemy
import redis, os
from dotenv import load_dotenv


load_dotenv()


db = SQLAlchemy()
redis_object = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0)
redis_object.ping()


from model.account import Account
from model.phonenumber import Phone_number