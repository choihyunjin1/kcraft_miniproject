from datetime import datetime, timezone
from flask import request, jsonify, current_app
from signals import signals_bp

# 고정 순서 카드 키워드
KEYWORDS = ["운동", "독서", "여행", "게임", "영화", "요리", "악기", "음악", "아이돌", "서브컬쳐"]

@signals_bp.route("/keywords", methods=["GET"])
def get_keywords():
    return jsonify({"result": "success", "keywords": KEYWORDS}), 200

# 카드 스와이프 API - 사용자 선호도 저장
@signals_bp.route("/swipe", methods=["POST"])
def save_swipe():
    db = current_app.config["DB"]
    data = request.get_json(silent=True) or request.form.to_dict()

    user_id = (data.get("user_id") or "").strip()
    index = data.get("index")
    direction = (data.get("direction") or "").strip().lower()  # left/right

    if not user_id or not isinstance(index, int) or direction not in ["left", "right"]:
        return jsonify({"result": "fail", "msg": "user_id, index(int), direction(left/right) 필수"}), 400
    if index < 0 or index >= len(KEYWORDS):
        return jsonify({"result": "fail", "msg": "index 범위 오류"}), 400

    keyword = KEYWORDS[index]
    value = 1 if direction == "right" else 0

    # users 컬렉션에 저장
    result = db.users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                f"signal_preferences.{keyword}": value,
                "signal_updated_at": datetime.now(timezone.utc),
            }
        }
    )

    if result.matched_count == 0:
        return jsonify({"result": "fail", "msg": "존재하지 않는 user_id"}), 404

    next_index = index + 1
    return jsonify({
        "result": "success",
        "saved": {keyword: value},
        "next_index": next_index,
        "done": next_index >= len(KEYWORDS)
    }), 200

# 결과 조회 API - 사용자의 선호도 프로필 반환
@signals_bp.route("/result", methods=["GET"])
def get_result():
    db = current_app.config["DB"]
    user_id = (request.args.get("user_id") or "").strip()

    if not user_id:
        return jsonify({"result": "fail", "msg": "user_id 필수"}), 400

    row = db.users.find_one({"user_id": user_id}, {"_id": 0, "signal_preferences": 1})
    if not row:
        return jsonify({"result": "fail", "msg": "존재하지 않는 user_id"}), 404

    return jsonify({
        "result": "success",
        "preferences": row.get("signal_preferences", {})
    }), 200