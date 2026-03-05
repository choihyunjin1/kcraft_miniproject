from pymongo import MongoClient
from datetime import datetime

from flask import Flask, render_template, jsonify, request
from bson import ObjectId
import re
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
# def home():
#     return render_template('index.html')

def home():
    user_id = (request.args.get("user_id") or "").strip()
    q = (request.args.get("q") or "").strip()

    query = {}
    if q:
        
        keyword = q.lstrip("#") 
        regex = {"$regex": keyword, "$options": "i"}
        query = {"tag": regex}

    all_post = list(db.posts.find(query).sort("created_at", -1))
    
    for post in all_post:
        post["_id"] = str(post["_id"])
        if user_id not in post.get('register', []):
            post['content'] = "dufthlwkarma"

    return render_template("index.html", posts=all_post, user_id=user_id, q=q)


###########################html 테스트용##################
@app.route('/postdetail')
def post_detail():
    # 나중엔 서버에서 진짜 댓글 데이터를 넘겨주겠지만, 지금은 UI 확인용!
    return render_template('postdetail.html')

@app.route('/mypage')
def mypage():
    user_id = (request.args.get("user_id") or "").strip()

    profile_name = "이름 없음"
    profile_user_id = user_id or "user_id 없음"
    profile_intro = "자기소개가 없습니다."
    my_post = []
    hobbies = [] # 초기화

    if user_id:
        user = db.users.find_one(
            {"user_id": user_id},
            {"_id": 0, "name": 1, "user_id": 1, "user_introduction": 1, "signal_preferences": 1} # signal_preferences 추가
        )
        if user:
            profile_name = user.get("name") or profile_name
            profile_user_id = user.get("user_id") or profile_user_id
            profile_intro = user.get("user_introduction") or profile_intro
            
            # 1값(선호)인 취미만 리스트로 추출
            prefs = user.get("signal_preferences", {})
            hobbies = [k for k, v in prefs.items() if v == 1]

        my_post = list(db.posts.find({"user_id": user_id}).sort("created_at", -1))
        for post in my_post:
            post["_id"] = str(post["_id"])

    return render_template(
        'mypage.html',
        profile_name=profile_name,
        profile_user_id=profile_user_id,
        profile_intro=profile_intro,
        hobbies=hobbies, # 추출한 hobbies 전달
        my_post=my_post,
        user_id=user_id,
    )

@app.route('/login')
def login():
    # 나중엔 서버에서 진짜 댓글 데이터를 넘겨주겠지만, 지금은 UI 확인용!
    return render_template('login.html')

@app.route('/register')
def register():
    # 나중엔 서버에서 진짜 댓글 데이터를 넘겨주겠지만, 지금은 UI 확인용!
    return render_template('register.html')

@app.route('/cardgame')
def cardgame():
    # 나중엔 서버에서 진짜 댓글 데이터를 넘겨주겠지만, 지금은 UI 확인용!
    return render_template('cardgame.html')

    
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