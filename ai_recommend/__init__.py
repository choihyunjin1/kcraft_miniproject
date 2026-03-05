from flask import Blueprint
ai_recommend_bp= Blueprint("ai_recommend", __name__)
from ai_recommend import routes