from datetime import datetime
from uuid import uuid4
from flask import request, jsonify, current_app
from bson import ObjectId
from bson.errors import InvalidId

from cardsets import cardsets_bp


@cardsets_bp.route("", methods=["POST"])
def create_cardset():
    db = current_app.config["DB"]
    data = request.get_json(silent=True) or {}

    user_id = (data.get("user_id") or "").strip()
    title = (data.get("title") or "내 카드셋").strip()

    if not user_id:
        return jsonify({"result": "fail", "msg": "user_id 필수"}), 400

    doc = {
        "owner_id": user_id,
        "title": title,
        "cards": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    res = db.card_sets.insert_one(doc)

    return jsonify({"result": "success", "set_id": str(res.inserted_id)}), 201


@cardsets_bp.route("/me", methods=["GET"])
def my_cardsets():
    db = current_app.config["DB"]
    user_id = (request.args.get("user_id") or "").strip()

    if not user_id:
        return jsonify({"result": "fail", "msg": "user_id 필수"}), 400

    rows = list(db.card_sets.find({"owner_id": user_id}))
    for r in rows:
        r["_id"] = str(r["_id"])
    return jsonify({"result": "success", "cardsets": rows}), 200


@cardsets_bp.route("/<set_id>/cards", methods=["POST"])
def add_card(set_id):
    db = current_app.config["DB"]
    data = request.get_json(silent=True) or {}

    word = (data.get("word") or "").strip()
    if not word:
        return jsonify({"result": "fail", "msg": "word 필수"}), 400

    try:
        oid = ObjectId(set_id)
    except (InvalidId, TypeError):
        return jsonify({"result": "fail", "msg": "잘못된 set_id"}), 400

    row = db.card_sets.find_one({"_id": oid})
    if not row:
        return jsonify({"result": "fail", "msg": "카드셋 없음"}), 404

    # 같은 카드 텍스트 중복 방지
    exists = any((c.get("text") or "").strip() == word for c in row.get("cards", []))
    if exists:
        return jsonify({"result": "fail", "msg": "이미 같은 카드가 있습니다."}), 409

    card = {"card_id": str(uuid4()), "text": word}
    db.card_sets.update_one(
        {"_id": oid},
        {"$push": {"cards": card}, "$set": {"updated_at": datetime.utcnow()}}
    )

    return jsonify({"result": "success", "card": card}), 200


@cardsets_bp.route("/<set_id>/cards/<card_id>", methods=["DELETE"])
def delete_card(set_id, card_id):
    db = current_app.config["DB"]
    oid = ObjectId(set_id)

    db.card_sets.update_one(
        {"_id": oid},
        {"$pull": {"cards": {"card_id": card_id}}, "$set": {"updated_at": datetime.utcnow()}}
    )

    return jsonify({"result": "success"}), 200


@cardsets_bp.route("/<set_id>", methods=["DELETE"])
def delete_cardset(set_id):
    db = current_app.config["DB"]

    try:
        oid = ObjectId(set_id)
    except (InvalidId, TypeError):
        return jsonify({"result": "fail", "msg": "잘못된 set_id"}), 400

    result = db.card_sets.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return jsonify({"result": "fail", "msg": "카드셋 없음"}), 404

    return jsonify({"result": "success", "msg": "카드셋 삭제 완료"}), 200