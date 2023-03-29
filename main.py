from flask_migrate import Migrate
from configuration.configs import Configs
from flask_app import create_app, db
from flask_app.base.models import User
from utility.logger import Logger
from flask_cors import CORS
import pickle
from flask import Flask, request, jsonify, g
import requests
import redis

app = create_app(Configs)
CORS(app)
Migrate(app, db)

# ******************************* Load model sent over HTTP **************************
# import base64
# def get_model_and_tokenizer():
#     response = requests.get(MODEL_SERVER_URL)
#     model_data = base64.b64decode(response.json()['model'].encode("utf-8"))
#     tokenizer_data = base64.b64decode(response.json()['tokenizer'].encode("utf-8"))
#     model = pickle.loads(model_data)
#     tokenizer = pickle.loads(tokenizer_data)
#     return model, tokenizer

# def load_model_and_tokenizer():
#     model_data = r.get("model")
#     tokenizer_data = r.get("tokenizer")
#     model = pickle.loads(model_data)
#     tokenizer = pickle.loads(tokenizer_data)
#     return model, tokenizer

@app.before_first_request
def load_redis():
    g.redis = redis.Redis(host='localhost', port=6379, db=0)

@app.before_first_request
def set_admin_user():
    user = User.query.filter_by(username='socialBlock').first()
    if not user:
        user = User(username='socialBlock', email='socialblock@gmail.com', password='admin@socialblock2023')
        db.session.add(user)
        db.session.commit()


if __name__ == "__main__":
    Logger().info('App is started!')
    app.run(host='0.0.0.0', port=Configs.port, debug=True, load_dotenv=True, use_reloader=True, use_debugger=False) 
