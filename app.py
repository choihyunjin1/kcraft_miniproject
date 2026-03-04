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


# open_ai
load_dotenv()
open_gpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Flask
app = Flask(__name__)

# mongodb connection in docker
client = MongoClient('mongodb://localhost:27017/')
db = client.dbjungle
app.logger.info(client.list_database_names()) # check the connection

#몽고 db id: mongodb+srv://admin:12345@name.scqpwqf.mongodb.net/

# main
@app.route('/')
def home():
    return render_template('index.html', post=postcard)


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


# post / create
@app.route('/post', methods=['POST'])
def post_my_info():
    input_content = request.form['input_content']
    author = request.form['user_name']
    tag = request.form.getlist['tags_list']

    post = {
        "author": author,
        "content": input_content,
        "created_at": datetime.now(),
        "likes": 0,
        "likers":[],
        "tag":tag,
        "comment":[]
    }

    db.posts.insert_one(post)
    return jsonify({'result': 'success', 'msg': '포스팅 성공!'})

# post / read_all
@app.route('/post', methods=['GET'])
def get_post():
    all_post = list(db.posts.find({}))
    for post in all_post:
        # 몽고디비 전용 ObjectId 객체를 그냥 가져오면 타입에러가 나니까 문자열로 바꿔줘야 함
        post['_id'] = str(post['_id'])

    return jsonify({'result': 'success', 'posts': all_post})


# post / read_user
@app.route('/post/<user_id>', methods=['GET'])
def get_my_post(user_id):
    user_post = list(db.posts.find({"author":user_id}))
    for post in user_post:
        post['_id'] = str(post['_id'])

    return jsonify({'result': 'success', 'posts': user_post})

# post / update_content
@app.route('/post/update', methods=['POST'])
def update_post_db():
   mg_idx = request.form['pass_idx']
   input_content = request.form['input_content']

   db.posts.update_one (
         {'_id': ObjectId(mg_idx)},
         {'$set': {
            'content': input_content
      }}
   )
   
   return jsonify({'result': 'success', 'msg': '수정 완료!'})


# post / delete_content
@app.route('/post/delete', methods=['POST'])
def delete_post_db():
    mg_idx = request.form['pass_idx']

    db.posts.delete_one (
        {'_id': ObjectId(mg_idx)}
    )

    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


# add_like_count
@app.route('/post/like', methods=['POST'])
def add_like_count():
    user_id = request.form['user_id']
    mg_idx = request.form['pass_idx']

    target_post = db.posts.find_one({'_id':ObjectId(mg_idx)})

    if user_id in target_post.get('likers',[]):
        db.posts.update_one(
        {'_id': ObjectId(mg_idx)},

        {'$inc': {'likes': -1},
            '$pull':{'likers':user_id}
        }
    )
        new_like_count = db.posts.find_one({'_id': ObjectId(mg_idx)})['likes']
   
        return jsonify({'result': 'success', 'likes': new_like_count})
    else:
        db.posts.update_one(
            {'_id': ObjectId(mg_idx)},
            {
            '$inc': {'likes': 1},
            '$addToSet':{'likers':user_id}
            }
    )
    
        new_like_count = db.posts.find_one({'_id': ObjectId(mg_idx)})['likes']
   
        return jsonify({'result': 'success', 'likes': new_like_count})

# comments - create
@app.route('/post/comment', methods=['POST'])
def comment_db():
   mg_idx = request.form['pass_idx']
   input_comment = request.form['input_comment']

   db.posts.update_one (
         {'_id': ObjectId(mg_idx)},
         {'$push': {
            'comment': input_comment
      }}
   )
   
   return jsonify({'result': 'success', 'msg': '댓글 작성 완료!'})

# comments / update
@app.route('/post/comment/update', methods=['POST'])
def update_comment_db():
   mg_idx = request.form['pass_idx']
   input_comment = request.form['input_comment']

   db.posts.update_one (
         {'_id': ObjectId(mg_idx)},
         {'$set': {
            'comment': input_comment
      }}
   )
   
   return jsonify({'result': 'success', 'msg': '댓글 수정 완료!'})


# comments/ delete_content
@app.route('/post/comment/delete', methods=['POST'])
def delete_comment_db():
    mg_idx = request.form['pass_idx']
    cmt_idx = request.form['comment_pass_idx']

    db.posts.update_one (
        {'_id': ObjectId(mg_idx)},
        {'$pull':
            {'comment':cmt_idx}
        }
    )

    return jsonify({'result': 'success', 'msg': '댓글 삭제 완료!'})



# 블루 프린트 등록 (회원가입)

app.register_blueprint(auth, url_prefix='/auth')
app.config["DB"] = db
db.users.create_index("user_id", unique=True)
#------------------------------

# 가챠 등록---------------------
from gacha import gacha_bp
app.register_blueprint(gacha_bp, url_prefix="/gacha")
#-------------------------------

# 카드 게임 등록----------------
from cardsets import cardsets_bp
app.register_blueprint(cardsets_bp)  

print(app.url_map)
#-------------------------------
if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)