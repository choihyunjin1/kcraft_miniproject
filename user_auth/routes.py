import os
import jwt
from datetime import datetime, timedelta, timezone
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
    user_mail = (data.get("user_mail") or "").strip()

    if not user_id or not password or not name or not user_mail or not gender:
        return jsonify({"result": "fail", "msg": "user_id, password, name, teg 필수"}), 400

    db = current_app.config["DB"]
    try:
        db.users.insert_one({
            "user_id": user_id,
            "password_hash": generate_password_hash(password),
            "name": name,
            "gender": gender,
            "created_at": datetime.now(timezone.utc),
            "user_mail": user_mail,
        })
    except DuplicateKeyError:
        return jsonify({"result": "fail", "msg": "이미 존재하는 user_id"}), 409

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