from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URL)
db = client["nexa_bot"]