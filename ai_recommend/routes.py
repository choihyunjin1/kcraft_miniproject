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

    my_infomation = list(db.users.find({"user_id":my_user_id}, 
                                       {"user_id": {"$ne": my_user_id}},
        {"password_hash":0, "created_at":0})
                         
                         )

def find_partner_candidates(my_user_id):
    db = current_app.config["DB"]

    partner_candidates_list = list(db.users.find(
        {"user_id": {"$ne": my_user_id}},
        {"password_hash":0, "created_at":0})
        )
    
    for partner_candidates_id in partner_candidates_list:
        partner_candidates_id['_id'] = str(partner_candidates_id['_id'])

    return partner_candidates_list


def make_prompt(my_user_id, card_result):
    template = textwrap.dedent(
        """
        너는 심리학적 분석과 소셜 매칭 데이터에 기반하여 사람들의 최적의 파트너를 찾아주는 **AI 관계 전문가(Relationship Expert)**이다.
        
        사용자의 정보: {my_user_id}
        파트너 후보군: {partner_candidates_list}
        """
        )