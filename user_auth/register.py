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

    if not user_id or not password or not name or not gender or not user_mail:
        return jsonify({
            "result": "fail",
            "msg": "user_id, password, name, gender, mail 은 필수입니다."
        }), 400

    
    return jsonify({
        "result": "success",
        "msg": "입력 검증 통과"
    }), 200