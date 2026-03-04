# kcraft_miniproject

hobby-matching-service/
│
├── app.py # Flask 메인 (모든 라우트 통합)

├── models.py # MongoDB 모델 전체 (User, Hobby, Match, Post)
├── utils.py # 유틸 함수 (DB 연결, 매칭 알고리즘, 세션)
├── config.py # 설정
├── requirements.txt # 패키지
├── .env # 환경 변수

├── static/  
│ ├── css/
│ │ └── style.css # 통합 CSS
│ ├── js/
│ │ └── main.js # 통합 JS (스와이프, AJAX)
│ └── images/
│ ├── hobbies/ # 취미 이미지
│ └── backgrounds/ # 하트/레인보우 배경
│

└── templates/ # Jinja2 템플릿
├── base.html # 기본 레이아웃 (상속용)
├── index.html # 랜딩
├── login.html # 로그인 (백엔드 완성)
├── register.html # 회원가입 (백엔드 완성)
├── swipe.html # 취미 스와이프
├── result.html # 매칭 결과 (if문으로 하트/레인보우 분기)
├── home.html # 홈 메인
├── gacha.html # 상자 뽑기
├── peek.html # 훔쳐보기
└── profile.html # 내 정보

├── .gitignore
├── README.md

## 변수명

몽고db 스키마?
users: { \_id, username, password_hash, gender, selected_hobbies, keys }
hobbies: { \_id, name, image_url, category }
matches: { \_id, user_id, matched_user_id, match_score }
posts: { \_id, author_id, target_user_id, content }

db 계정:mongodb+srv://admin:12345@name.scqpwqf.mongodb.net/

변수명:
user_id = 유저 아이디
password = 유저 비번
name = 유저 이름
gender = 유저 성별
user_mail = 유저 메일
