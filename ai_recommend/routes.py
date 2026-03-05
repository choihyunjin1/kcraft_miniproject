import os
from openai import OpenAI
from dotenv import load_dotenv
import textwrap
import json
from flask import Blueprint, request, jsonify, current_app
from ai_recommend import ai_recommend_bp


# open_ai
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
        만일 'signal_preferences' 계산 시 동점이 나온다면 'user_introduction'에 가중치를 두어 'partner_score'에서 동점자가 나오지 않도록 하시오.
        reason은 400 내외의 분량을 유지하고, 톤은 사용자가 친금감을 느낄 수 있도록 존칭을 사용하고, 나한테 인사하지마시오 파트너와 어떻게 친해질 수 있는지 방안을 제시하시오.


        [출력 형식]
        결과는 반드시 지정된 JSON 스키마에 맞추어 배열 형태로 반환하시오.
        """
        )
    
    return template

#

# my_user_id = 'mj_1201'

@ai_recommend_bp.route('/<user_id>', methods=['GET'])
def get_ai_comment(user_id):
    try:
        my_infomation, jungle_batch, jungle_class = find_my_info(user_id)
        partner_candidates_list = find_partner_candidates(user_id, jungle_batch, jungle_class)
        template = make_prompt(my_infomation, partner_candidates_list)

        response = openai_client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role":"developer", "content":"사용자가 가장 잘 맞는 파트너 3명을 추천해주세요"},
                {"role":"user", "content":template}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "best_partner_info",
                    "schema": {

                        "type": "object",
                        "properties": {
                            "partners": {
                                "type": "array",
                                "minItems": 3,
                                "maxItems": 3,
                                "items":{
                                    "type": "object",
                                    "properties": {
                                        "best_partner": {
                                            "type": "string"
                                        },
                                        "best_partner_id": {
                                            "type": "string"
                                        },
                                        "partner_score": {
                                            "type": "integer"
                                        },
                                        "reason": {
                                            "type": "string"
                                        }
                                    },
                                    "required": ["best_partner", "best_partner_id", "partner_score", "reason"],
                                    "additionalProperties": False
                                }
                            },
                        },
                        "required": ["partners"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )

        # 이 방식이 더 안전
        ai_answer = json.loads(response.output_text)

        # 프론트와 형식 맞추기
        return jsonify({"result": "success", **ai_answer}), 200

    except Exception as e:
        return jsonify({"result": "fail", "msg": str(e)}), 500

