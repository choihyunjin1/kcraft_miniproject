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




# Flask
app = Flask(__name__)



#몽고 db id: mongodb+srv://admin:12345@name.scqpwqf.mongodb.net/

# main
@app.route('/')
def home():
    return render_template('index.html')


###########################html 테스트용##################
@app.route('/postdetail')
def post_detail():
    # 나중엔 서버에서 진짜 댓글 데이터를 넘겨주겠지만, 지금은 UI 확인용!
    return render_template('postdetail.html')

@app.route('/mypage')
def mypage():
    # 나중엔 서버에서 진짜 댓글 데이터를 넘겨주겠지만, 지금은 UI 확인용!
    return render_template('mypage.html')
#########################################

# blue print - post, comment, likes
from posts.routes import posts_bp
app.register_blueprint(posts_bp)

# blue print - ai recommend
from ai_recommend import ai_recommend_bp
app.register_blueprint(ai_recommend_bp, url_prefix="/ai_recommend")

# 블루 프린트 등록 (회원가입)
app.register_blueprint(auth, url_prefix='/auth')
app.config["DB"] = db
db.users.create_index("user_id", unique=True)
db.users.create_index([("jungle_batch", 1), ("jungle_class", 1)])
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

# 열쇠 개수 주입기-----------------
@app.context_processor
def inject_key_count():
    user_id = (request.args.get("user_id") or "").strip()
    key_count = 0 
    if user_id:
        user = db.users.find_one({"user_id": user_id}, {"_id": 0, "key_count": 1})
        if user:
            key_count = user.get("key_count", 0)
    return {"key_count": key_count}
#-------------------------------
if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)