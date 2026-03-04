from flask import Blueprint

cardsets_bp = Blueprint("cardsets", __name__, url_prefix="/cardsets")

from cardsets import routes