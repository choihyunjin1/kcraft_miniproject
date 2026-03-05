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
teg = ?
card_id = 카드셋 용 아이디
postcard = 프런트 사람들 정보 카드

## 데이터베이스(MongoDB) 스키마 정의

| **필드명 (Key)** | **데이터 타입** | **설명**                                       |
| ---------------- | --------------- | ---------------------------------------------- |
| `_id`            | `ObjectId`      | 몽고디비 고유 문서 ID (조회 시 `str`변환 필요) |
| `author`         | `String`        | 작성자의 아이디 또는 이름                      |
| `content`        | `String`        | 게시글 또는 댓글의 본문 내용                   |
| `created_at`     | `DateTime`      | 생성 날짜 및 시간                              |
| `likes`          | `Integer`       | 좋아요 총 개수                                 |
| `likers`         | `Array(String)` | 좋아요를 누른 사용자들의 아이디 리스트         |
| `tag`            | `Array(String)` | 게시글에 달린 태그 목록                        |
| `comment`        | `Array(String)` | 게시글에 달린 댓글 목록                        |

## API 요청 파라미터 (Request Keys)

| **파라미터명**     | **설명**             | **비고**                                |
| ------------------ | -------------------- | --------------------------------------- |
| `user_name`        | 작성자 이름          | 게시글 생성 시 사용                     |
| `input_content`    | 입력 본문 내용       | 게시글 작성 및 수정 시 사용             |
| `tags_list`        | 태그 리스트          | `request.form.getlist`로 수집           |
| `pass_idx`         | **게시글 고유 ID**   | `mg_idx`변수로 받아 `ObjectId`로 변환됨 |
| `user_id`          | 현재 사용자 아이디   | 좋아요 기능에서 본인 확인용             |
| `input_comment`    | 댓글 내용            | 댓글 작성 및 수정 시 사용               |
| `comment_pass_idx` | **삭제할 댓글 내용** | `cmt_idx`변수로 받아 `$pull`연산에 사용 |

## 주요 비즈니스 로직 변수

| **변수명**           | **출처 / 생성 위치**                | **역할 및 비즈니스 의미**                                                      |
| -------------------- | ----------------------------------- | ------------------------------------------------------------------------------ |
| **`app`**            | `Flask(__name__)`                   | 전체 웹 서비스를 구동하고 관리하는 서버 객체입니다.                            |
| **`db`**             | `client.dbjungle`                   | 몽고디비(`dbjungle`) 데이터베이스와 소통하는 연결 객체입니다.                  |
| **`mg_idx`**         | `request.form['pass_idx']`          | **게시글의 고유 번호**입니다. 수정, 삭제, 좋아요 시 대상을 찾는 기준이 됩니다. |
| **`author`**         | `request.form['user_name']`         | 게시글을 작성한**사용자의 이름**을 저장합니다.                                 |
| **`input_content`**  | `request.form['input_content']`     | 사용자가 작성하거나 수정한**게시글 본문**데이터입니다.                         |
| **`tag`**            | `request.form.getlist('tags_list')` | 한 게시글에 달린**여러 개의 태그 뭉치** (리스트)입니다.                        |
| **`all_post`**       | `db.posts.find({})`                 | 데이터베이스에서 긁어온**전체 게시글 목록**입니다.                             |
| **`target_post`**    | `db.posts.find_one()`               | 좋아요 기능을 처리하기 위해 임시로 불러온**특정 게시글 정보**입니다.           |
| **`new_like_count`** | `db.posts.find_one()...['likes']`   | 좋아요 클릭 후 업데이트된**최종 하트 숫자**입니다.                             |
| **`input_comment`**  | `request.form['input_comment']`     | 사용자가 새로 입력한**댓글 텍스트**데이터입니다.                               |
| **`cmt_idx`**        | `request.form['comment_pass_idx']`  | 삭제 요청이 들어온**특정 댓글의 내용**을 담는 변수입니다.                      |

## API

| **기능**         | **주소 (Route)**       | **메서드** |
| ---------------- | ---------------------- | ---------- |
| 전체 게시글 조회 | `/post`                | `GET`      |
| 게시글 작성      | `/post`                | `POST`     |
| 게시글 수정      | `/post/update`         | `POST`     |
| 게시글 삭제      | `/post/delete`         | `POST`     |
| 좋아요 토글      | `/post/like`           | `POST`     |
| 댓글 작성        | `/post/comment`        | `POST`     |
| 댓글 삭제        | `/post/comment/delete` | `POST`     |


---------------------테스트 계정----------------------
