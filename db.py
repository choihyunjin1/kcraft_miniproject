from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# mongodb connection in docker
client = MongoClient('mongodb://localhost:27017/')
db = client.dbjungle
# app.logger.info(client.list_database_names()) # check the connection