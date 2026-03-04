import random
from flask import request, jsonify, current_app
from datetime import datetime
from gacha import gacha_bp

@gacha_bp.route("/draw", methods=["POST"])
def draw():
    picked_number = random.randint(0, 3) 

    return jsonify({
        "result": "success",
        "picked": picked_number
    }), 200