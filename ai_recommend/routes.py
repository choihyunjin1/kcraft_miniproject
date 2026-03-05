import os
from openai import OpenAI
from dotenv import load_dotenv
import textwrap

from flask import request, jsonify, current_app


# open_ai
load_dotenv()
open_gpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 
def find_my_info(my_user_id):
    db = current_app.config["DB"]

    my_infomation = db.users.find_one(
        {"user_id":my_user_id}, 
        {"password_hash":0, "created_at":0, "user_mail":0, "signal_updated_at":0})
    

    my_infomation['_id'] = str(my_infomation['_id'])

    jg_batch = my_infomation["jungle_batch"]
    jg_class = my_infomation["jungle_class"]
    return my_infomation, jg_batch, jg_class

def find_partner_candidates(my_user_id, jg_batch, jg_class):
    db = current_app.config["DB"]

    partner_candidates_list = list(db.users.find(
        {"user_id": {"$ne": my_user_id}, "jungle_batch":jg_batch, "jungle_class":jg_class, "signal_game_done":True},
        {"password_hash":0, "created_at":0, "user_mail":0, "signal_updated_at":0})
        )
    
    for partner_candidates_id in partner_candidates_list:
        partner_candidates_id['_id'] = str(partner_candidates_id['_id'])

    return partner_candidates_list


def make_prompt(my_infomation, partner_candidates_list):
    template = textwrap.dedent(
        f"""
        [역할]
        너는 데이터를 기반으로 최적의 파트너를 찾아주는 **AI 관계 전문가(Relationship Expert)**이다.

        [데이터 입력 및 설명]
        사용자와 파트너 후보군의 정보는 아래를 참고하라.
        - 사용자의 정보 : {my_infomation}
        - 파트너 후보군의 정보 : {partner_candidates_list}
        - 취미에 대한 선호도 : 사용자 및 파트너 후보군 정보 내의 'signal_preferences'필드. 1(선호)과 0(비선호).

        [임무]
        사용자의 'signal_preferences'과 'user_introduction'의 일치율을 분석하여 사용자와 가장 합이 잘 맞을 것 같은 최적의 파트너 3명을 선정하라.
        partner_score는 동점자가 나오지 않도록 하시오.

        [출력 형식(JSON)]
        반드시 아래의 JSON 배열 형식으로만 답변하시오.
        [
            {{
            "best_partner":"name",
            "best_partner_id":"user_id",
            "partner_score": 1~100 사이의 정수,
            "reason":300자 내외의 문자열
            }}
        ]

        """
        )
    
    return template

my_user_id = 'mj_1201'
