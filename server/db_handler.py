from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import uuid
import ssl
import json

mongo_uri = "**********************************************"
client = MongoClient(mongo_uri, ssl_cert_reqs=ssl.CERT_NONE)

mydb = client["todo_database"]
tasks_collection = mydb["tasks"]
users_collection = mydb["users"]
