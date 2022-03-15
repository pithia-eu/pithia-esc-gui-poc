from pymongo import MongoClient
import environ

env = environ.Env()

client = MongoClient(env('MONGODB_CONNECTION_STRING'))
db = client[env('DB_NAME')]