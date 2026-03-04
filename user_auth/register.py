from flask import request, jsonify
from user_auth import auth

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or request.form.to_dict()

    user_id = (data.get("user_id") or "").strip()
    password = (data.get("password") or "").strip()
    name = (data.get("name") or "").strip()
    gender = (data.get("gender") or "").strip()
    user_mail = (data.get("user_mail") or "").strip()
    user_introcution = (data.get("user_introduction") or "").strip()

    if not user_id or not password or not name or not gender or not user_mail or not user_introcution:
        return jsonify({
            "result": "fail",
            "msg": "아이디, 비밀번호, 성함, 성별, 이메일 , 자기소개 은 필수입니다."
        }), 400

    
    return jsonify({
        "result": "success",
        "msg": "입력 검증 통과"
    }), 200