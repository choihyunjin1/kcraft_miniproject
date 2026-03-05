import os
import jwt
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import DuplicateKeyError

from user_auth import auth

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "60"))

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or request.form.to_dict()
    user_id = (data.get("user_id") or "").strip()
    password = (data.get("password") or "").strip()
    name = (data.get("name") or "").strip()
    gender = (data.get("gender")  or "").strip()
    user_introduction = (data.get("user_introduction") or "").strip()

    jungle_batch = (data.get("jungle_batch") or "").strip() 
    jungle_class = (data.get("jungle_class") or "").strip()  

    if not user_id or not password or not name or not gender or not user_introduction or not jungle_batch or not jungle_class:
        return jsonify({"result": "fail", "msg": "user_id, password, name, gender, user_introduction, jungle_batch, jungle_class 필수"}), 400

    db = current_app.config["DB"]
    try:
        db.users.insert_one({
            "user_id": user_id,
            "password_hash": generate_password_hash(password),
            "name": name,
            "gender": gender,
            "created_at": datetime.now(timezone.utc),
            "user_introduction": user_introduction,

           
            "jungle_batch": jungle_batch,
            "jungle_class": jungle_class,
            "key_count": 20
        })
    except DuplicateKeyError:
        return jsonify({"result": "fail", "msg": "이미 존재하는 아이디"}), 409

    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXPIRES_MIN)).timestamp()),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "result": "success",
        "msg": "회원가입 성공",
        "access_token": token,
        "token_type": "Bearer"
    }), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or request.form.to_dict()
    user_id = (data.get("user_id") or "").strip()
    password = (data.get("password") or "").strip()

    if not user_id or not password:
        return jsonify({"result": "fail", "msg": "user_id, password 필수"}), 400

    db = current_app.config["DB"]
    user = db.users.find_one({"user_id": user_id})
    if not user or not check_password_hash(user.get("password_hash", ""), password):
        return jsonify({"result": "fail", "msg": "아이디 또는 비밀번호 오류"}), 401

    grant_weekly_key_if_due(db, user_id)

    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXPIRES_MIN)).timestamp()),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "result": "success",
        "msg": "로그인 성공",
        "access_token": token,
        "token_type": "Bearer"
    }), 200

@auth.route("/group-members", methods=["GET"])
def group_members():
    db = current_app.config["DB"]
    user_id = (request.args.get("user_id") or "").strip()
    if not user_id:
        return jsonify({"result": "fail", "msg": "user_id 필수"}), 400
    
    me = db.users.find_one({"user_id": user_id}, {"_id": 0, "jungle_batch": 1, "jungle_class": 1})
    if not me:
        return jsonify({"result": "fail", "msg": "존재하지 않는 user_id"}), 404

    members = list(db.users.find(
        {
            "jungle_batch": me["jungle_batch"],
            "jungle_class": me["jungle_class"]
        },
        {
            "_id": 0,
            "password_hash": 0,
            "key_count": 0
        }
    ))

    return jsonify({
        "result": "success",
        "group": {
            "jungle_batch": me["jungle_batch"],
            "jungle_class": me["jungle_class"]
        },
        "count": len(members),
        "members": members
    }), 200

def current_weekly_token_kst():
    kst = ZoneInfo("Asia/Seoul")
    now_kst = datetime.now(kst)

    # weekday: 월0 화1 수2 목3 ...
    days_since_thursday = (now_kst.weekday() - 3) % 7
    last_thursday = (now_kst - timedelta(days=days_since_thursday)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # 같은 주의 목요일 00:00 기준 토큰
    return last_thursday.strftime("%Y-%m-%d")


def grant_weekly_key_if_due(db, user_id: str):
    token = current_weekly_token_kst()

    # 아직 이번 주 토큰으로 지급 안 된 경우에만 +1
    db.users.update_one(
        {
            "user_id": user_id,
            "$or": [
                {"last_weekly_key_token": {"$exists": False}},
                {"last_weekly_key_token": {"$ne": token}},
            ],
        },
        {
            "$inc": {"key_count": 1},
            "$set": {
                "last_weekly_key_token": token,
                "last_weekly_key_at": datetime.now(timezone.utc),
            },
        },
    )