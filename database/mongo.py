from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users = db.users
numbers = db.numbers
orders = db.orders