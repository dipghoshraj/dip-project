from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from dotenv import load_dotenv
import os
from model import db
from handler.inbound import inbound_ops
from handler.authenticate import validdec


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

db.init_app(app)
api = Api(app)


@app.route('/api/inbound', methods=['POST'])
@validdec
def inbound(data):
    try:
        ret_data, code = inbound_ops(data)
        return jsonify(ret_data), code
    except Exception as e:
        return jsonify({'message': '', 'error': 'unknown faliure'}), 500

@app.route('/api/outbound', methods=['POST'])
@validdec
def outbound(data):
    try:
        return jsonify({'message': '', 'error': 'unknown faliur'}), 200
    except Exception as e:
        return jsonify({'message': '', 'error': 'unknown faliure'}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
    