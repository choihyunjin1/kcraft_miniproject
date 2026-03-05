import os
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
import random
from db import db

KEYWORDS = ["운동", "독서", "여행", "게임", "영화", "요리", "악기", "음악", "아이돌", "서브컬쳐",
            "뷰티", "동물", "패션", "사진", "커피", "술", "차", "자전거", "자동차", "캠핑",
            "등산", "낚시", "봉사활동", "명상", "요가", "코딩", "외국어", "주식", "암호화폐", 
            "재테크", "심리학", "철학", "역사", "과학", "기술", "사회문제"]

users_to_insert = []

for i in range(1, 11):
    user_id = f"testuser_{i:02d}"
    
    preferences = {kw: random.choice([0, 1]) for kw in KEYWORDS}
    
    doc = {
        "user_id": user_id,
        "password_hash": generate_password_hash("Pass1234!"), 
        "name": f"김정글{i}호",
        "gender": random.choice(["male", "female"]),
        "created_at": datetime.now(timezone.utc),
        "user_mail": f"{user_id}@example.com",
        "user_introduction": f"안녕하세요! 저는 {user_id}입니다. 테스트를 위해 생성된 계정입니다.",
        "jungle_batch": "12",
        "jungle_class": "303",
        "key_count": 5,
        "signal_game_done": True,
        "signal_updated_at": datetime.now(timezone.utc),
        "signal_preferences": preferences
    }
    users_to_insert.append(doc)

if __name__ == "__main__":
    result = db.users.insert_many(users_to_insert)
    print(f"완료! 삽입된 Document 개수: {len(result.inserted_ids)}")
    print("공통 비밀번호: Pass1234!")
