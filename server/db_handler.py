from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import uuid
import ssl
import json
import config

mongo_uri = config.MONGO_URI
client = MongoClient(mongo_uri, ssl_cert_reqs=ssl.CERT_NONE)

mydb = client[config.MY_DB]
tasks_collection = mydb[config.TASKS_COLLECTION]
users_collection = mydb[config.USERS_COLLECTION]
