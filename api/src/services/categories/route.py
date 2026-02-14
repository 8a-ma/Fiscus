import json
from . import service as s
# from services.factory import services
from flask import Blueprint, abort, Response


categories_bp = Blueprint('categories', __name__, url_prefix='/v1/categories')


@categories_bp.get("")
def get_all_categories():
    return Response(json.dumps(s.get_all_categories()), status=200, mimetype='application/json')
