from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pickle
import redis

model_name = 'sentence-transformers/paraphrase-distilroberta-base-v1'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()

# *********************** Send the loaded model over HTTP ********************
# import base64
# from fastapi import FastAPI
# app = FastAPI()
# @app.get("/load_model")
# async def load_model():
#     model_data = base64.b64encode(pickle.dumps(model)).decode("utf-8")
#     tokenizer_data = base64.b64encode(pickle.dumps(tokenizer)).decode("utf-8")
#     return {"model": model_data, "tokenizer": tokenizer_data}

r = redis.Redis(host='localhost', port=6379, db=0)
model_data = pickle.dumps(model)
tokenizer_data = pickle.dumps(tokenizer)
r.set("model", model_data)
r.set("tokenizer", tokenizer_data)