from flask import Blueprint
cardsets_bp = Blueprint("cardsets", __name__)
from cardsets import routes