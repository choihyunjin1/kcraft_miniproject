from flask import Blueprint

auth = Blueprint('auth', __name__)

from user_auth import routes
