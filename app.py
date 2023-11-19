from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
import os
from model import db
from handler.inbound import inbound_ops
from handler.authenticate import validdec, api_call_limit
from handler.outbound import outbound_ops


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

db.init_app(app)
api = Api(app)


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "hello world"}), 200


@app.route('/inbound/sms/', methods=['POST'])
@validdec
def inbound(data):
    try:
        ret_data, code = inbound_ops(data)
        return jsonify(ret_data), code
    except Exception as e:
        return jsonify({'message': '', 'error': 'unknown faliure'}), 500




@app.route('/outbound/sms/', methods=['POST'])
@api_call_limit
@validdec
def outbound(data):
    try:
        outbound_resp, code = outbound_ops(data)
        return jsonify(outbound_resp), code
    except Exception as e:
        print(e)
        return jsonify({'message': '', 'error': 'unknown faliure'}), 500
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    