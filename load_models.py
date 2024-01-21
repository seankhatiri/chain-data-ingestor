# # Uncomment
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import pickle
# import redis

# model_name = 'sentence-transformers/paraphrase-distilroberta-base-v1'
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)
# model.eval()

# r = redis.Redis(host='localhost', port=6379, db=0)
# model_data = pickle.dumps(model)
# tokenizer_data = pickle.dumps(tokenizer)
# r.set("model", model_data)
# r.set("tokenizer", tokenizer_data)