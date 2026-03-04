from flask import Blueprint
cardsets_bp = Blueprint("ai_recommend", __name__)
from ai_recommend import routes