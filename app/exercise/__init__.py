from flask import Blueprint

bp = Blueprint('exercise',__name__)

from app.exercise import routes