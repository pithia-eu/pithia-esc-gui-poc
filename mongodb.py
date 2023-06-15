import certifi
import environ
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

env = environ.Env()

try:
    # If using local MongoDB deployment
    client = MongoClient(env('MONGODB_CONNECTION_STRING'), serverSelectionTimeoutMS=1)
except ServerSelectionTimeoutError:
    client = MongoClient(env('MONGODB_CONNECTION_STRING'), tlsCAFile=certifi.where())
db = client[env('MIGRATION_TEST_MONGODB_NAME')]