import random
from flask import request, jsonify, current_app
from gacha import gacha_bp


@gacha_bp.route("/draw", methods=["POST"])
def draw():
    db = current_app.config["DB"]
    data = request.get_json(silent=True) or request.form.to_dict()
    user_id = (data.get("user_id") or "").strip()

    if not user_id:
        return jsonify({"result": "fail", "msg": "user_id 필수"}), 400

    # 1) 열쇠 1개 소모 (1개 이상 있을 때만)
    consume_result = db.users.update_one(
        {"user_id": user_id, "key_count": {"$gte": 1}},
        {"$inc": {"key_count": -1}}
    )

    if consume_result.matched_count == 0:
        user_exists = db.users.find_one({"user_id": user_id}, {"_id": 0, "user_id": 1})
        if not user_exists:
            return jsonify({"result": "fail", "msg": "존재하지 않는 user_id"}), 404
        return jsonify({"result": "fail", "msg": "열쇠가 부족합니다."}), 400

    # 2) 0~3개 랜덤 획득
    picked_number = random.randint(0, 3)

    db.users.update_one(
        {"user_id": user_id},
        {"$inc": {"key_count": picked_number}}
    )

    user = db.users.find_one({"user_id": user_id}, {"_id": 0, "key_count": 1})

    return jsonify({
        "result": "success",
        "picked": picked_number,
        "key_count": user.get("key_count", 0)
    }), 200


@gacha_bp.route("/my-keys", methods=["GET"])
def my_keys():
    db = current_app.config["DB"]
    user_id = (request.args.get("user_id") or "").strip()

    if not user_id:
        return jsonify({"result": "fail", "msg": "user_id 필수"}), 400

    user = db.users.find_one({"user_id": user_id}, {"_id": 0, "key_count": 1})
    if not user:
        return jsonify({"result": "fail", "msg": "존재하지 않는 user_id"}), 404

    return jsonify({
        "result": "success",
        "key_count": user.get("key_count", 0)
    }), 200

