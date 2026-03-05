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




# 12번째 테스터 (남성 가상 인물)
user_id_12 = "testuser_12_m"
preferences_12 = {kw: random.choice([0, 1]) for kw in KEYWORDS}
doc_12 = {
    "user_id": user_id_12,
    "password_hash": generate_password_hash("Pass1234!"), 
    "name": "성시경팀장",
    "gender": "male",
    "created_at": datetime.now(timezone.utc),
    "user_introduction": "안녕하세요, 저는 주말마다 바이크를 타고 근교로 나가는 것을 좋아합니다. 요즘은 요리에도 취미가 생겨서 파스타나 스테이크를 자주 해 먹곤 해요. 활동적이고 긍정적인 에너지를 가진 분과 대화를 나누면 좋겠습니다.",
    "jungle_batch": "12",
    "jungle_class": "303",
    "key_count": 5,
    "signal_game_done": True,
    "signal_updated_at": datetime.now(timezone.utc),
    "signal_preferences": preferences_12
}
users_to_insert.append(doc_12)

# 13번째 테스터 (여성 가상 인물)
user_id_13 = "testuser_13_f"
preferences_13 = {kw: random.choice([0, 1]) for kw in KEYWORDS}
doc_13 = {
    "user_id": user_id_13,
    "password_hash": generate_password_hash("Pass1234!"), 
    "name": "아이유대리",
    "gender": "female",
    "created_at": datetime.now(timezone.utc),
    "user_introduction": "조용한 카페에서 책을 읽거나 맛있는 요리를 함께 만들어 먹는 소소한 일상을 즐깁니다. 가끔 스트레스 받을 때는 신나는 음악을 틀어놓고 드라이브를 하기도 해요. 따뜻하고 배려심 깊은 분과 소통하고 싶습니다.",
    "jungle_batch": "12",
    "jungle_class": "303",
    "key_count": 5,
    "signal_game_done": True,
    "signal_updated_at": datetime.now(timezone.utc),
    "signal_preferences": preferences_13
}
users_to_insert.append(doc_13)

if __name__ == "__main__":
    result = db.users.insert_many(users_to_insert)
    print(f"완료! 삽입된 Document 개수: {len(result.inserted_ids)}")
    print("공통 비밀번호: Pass1234!")
