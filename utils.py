from pymongo import MongoClient
import environ

env = environ.Env()
print(env('MONGODB_CONNECTION_STRING'))

client = MongoClient(env('MONGODB_CONNECTION_STRING'))
db = client[env('DB_NAME')]