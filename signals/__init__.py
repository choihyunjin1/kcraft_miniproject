from flask import Blueprint

signals_bp = Blueprint("signals", __name__)

from signals import routes