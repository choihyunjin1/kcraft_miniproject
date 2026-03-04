from pymongo import MongoClient
from datetime import datetime

from flask import Flask, render_template, jsonify, request
from bson import ObjectId

import os
from openai import OpenAI
from dotenv import load_dotenv

# open_ai
load_dotenv()
open_gpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Flask
app = Flask(__name__)

# mongodb connection in docker
client = MongoClient('mongodb://localhost:27017/')
db = client.dbjungle


# main
@app.route('/')
def home():
   return render_template('index.html')


# userid, pw, name, gender, card_result
db.users.insert_one({"user_id": "admin", "pw": "1234", 
                     "name":"minjeong", "gender": "female", 
                     "card_result":"1111",
                     "game_key":"3"})

# insert hobby_card
hobby = ["campping", "dance", "K-pop", "game"] # here
hobby_card = [{"card_list" : i} for i in hobby]
db.card_content.insert_many(hobby_card)

# board
db.posts.insert_one({
    "author": "minjeong",
    "content": "content ",
    "created_at": datetime.now(),
    "likes": 0
})

print(client.list_database_names())