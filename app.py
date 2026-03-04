from pymongo import MongoClient
from datetime import datetime

from flask import Flask, render_template, jsonify, request
from bson import ObjectId

import os
from openai import OpenAI
from dotenv import load_dotenv
from user_auth import auth

from functools import wraps
import jwt
from bson.errors import InvalidId

from db import db
from posts.routes import posts_bp



# Flask
app = Flask(__name__)



#몽고 db id: mongodb+srv://admin:12345@name.scqpwqf.mongodb.net/

# main
@app.route('/')
def home():
    return render_template('index.html')


# userid, pw, name, gender, card_result
# db.users.insert_one({"user_id":"admin", "pw": "1234", 
#                      "name":"minjeong", "gender": "female", 
#                      "card_result":"1111",
#                      "game_key":"3"})


# insert hobby_card
# hobby = ["campping", "dance", "K-pop", "game"] # here
# hobby_card = [{"card_list" : i} for i in hobby]
# db.card_content.insert_many(hobby_card)

# board
# db.posts.insert_one({
#     "author": "minjeong",
#     "content": "content ",
#     "created_at": datetime.now(),
#     "likes": 0,
#     "likers":[],
#     "tag":[]
# })


# blue print - post, comment, likes
app.register_blueprint(posts_bp)



# 블루 프린트 등록 (회원가입)
app.register_blueprint(auth, url_prefix='/auth')
app.config["DB"] = db
db.users.create_index("user_id", unique=True)
#------------------------------

# 가챠 등록---------------------
from gacha import gacha_bp
app.register_blueprint(gacha_bp, url_prefix="/gacha")
#-------------------------------

# 카드 셋 등록 제작기-------------
# from cardsets import cardsets_bp
# app.register_blueprint(cardsets_bp)  
from cardsets import cardsets_bp
app.register_blueprint(cardsets_bp, url_prefix="/cardsets")
print(app.url_map)
#-------------------------------

# 카드 게임 등록-----------------
from signals import signals_bp
app.register_blueprint(signals_bp, url_prefix="/signals")
#-------------------------------

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)