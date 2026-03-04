from flask import Blueprint

gacha_bp = Blueprint("gacha", __name__)

from gacha import routes  