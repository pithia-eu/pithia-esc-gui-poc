from pymongo import MongoClient
import environ
import certifi

env = environ.Env()

client = MongoClient(env('MONGODB_CONNECTION_STRING'), tlsCAFile=certifi.where())
db = client[env('DB_NAME')]