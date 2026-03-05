from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from db import db
from flask import render_template

posts_bp = Blueprint('posts', __name__)

# post / create
@posts_bp.route('/post', methods=['POST'])
def post_my_info():
    user_id = (request.args.get("user_id") or "").strip()
    input_content = request.form['input_content']
    #author = request.form['user_name']
    user = db.users.find_one({"user_id": user_id}, {"_id": 0, "name": 1})
    author = user.get("name") if user and user.get("name") else user_id
    tag = request.form.getlist('tags_list')

    post = {
        "user_id": user_id,
        "author": author,
        "content": input_content,
        "created_at": datetime.now(),
        "likes": 0,
        "likers":[],
        "tag":tag,
        "comment":[],
        "register":[user_id]
    }

    db.posts.insert_one(post)
    # return jsonify({'result': 'success', 'msg': '포스팅 성공!'})
    return render_template('index.html', posts=post)

# post / read_all
@posts_bp.route('/post', methods=['GET'])
def get_post():
    user_id = (request.args.get("user_id") or "").strip()

    all_post = list(db.posts.find({}))

    for post in all_post:
        # 몽고디비 전용 ObjectId 객체를 그냥 가져오면 타입에러가 나니까 문자열로 바꿔줘야 함
        post['_id'] = str(post['_id'])

        if user_id not in post.get('register', []):
            post['content'] = "열쇠를 사용하여 잠금을 해제하세요!"

    # return jsonify({'result': 'success', 'posts': all_post})
    return render_template('index.html', posts=all_post)

# post / read_user
@posts_bp.route('/mypage', methods=['GET'])
def get_my_post():
    # check login status
    user_id = (request.args.get("user_id") or "").strip()

    # maybe...
    if not user_id:
        return render_template('mypage.html', my_post=[])

    user_post = list(db.posts.find({"user_id":user_id}))
    for post in user_post:
        post['_id'] = str(post['_id'])

    return render_template('mypage.html', my_post=user_post)
    # return jsonify({'result': 'success', 'posts': user_post})

# post / read_one
@posts_bp.route('/post/detail/', methods=['GET'])
def get_one_post():
    user_id = (request.args.get("user_id") or "").strip()
    # js에서 보낸 pass_idx를 request를 통해 받음
    mg_idx = request.args.get("pass_idx")
    # # 특정 결과 값을 뽑아 보기 / str -> mongo의 오브젝트 id로 다시 변환
    one_post = db.posts.find_one({'_id': ObjectId(mg_idx)})
    one_post['_id'] = str(one_post['_id'])

    if user_id not in one_post.get('register', []):
        one_post['content'] = "열쇠를 사용하여 잠금을 해제하세요!"

    # return jsonify({'result': 'success', 'memo': one_post})
    return render_template('postdetail.html', post=one_post)

# post / update_content
@posts_bp.route('/post/update', methods=['POST'])
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
@posts_bp.route('/post/delete', methods=['POST'])
def delete_post_db():
    mg_idx = request.form['pass_idx']

    db.posts.delete_one (
        {'_id': ObjectId(mg_idx)}
    )

    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


# add_like_count
@posts_bp.route('/post/like', methods=['POST'])
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
@posts_bp.route('/post/comment', methods=['POST'])
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
@posts_bp.route('/post/comment/update', methods=['POST'])
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
    # return render_template('index.html', posts=input_comment)


# comments/ delete_content
@posts_bp.route('/post/comment/delete', methods=['POST'])
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

