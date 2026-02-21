import json
from . import service as s
from services.factory import services
from flask import Blueprint, abort, Response
from decorators.Keys_required import RequiredKeys


categories_bp = Blueprint('categories', __name__, url_prefix='/v1/categories')


@categories_bp.get("")
def get_all_categories():
    return Response(json.dumps(s.get_all_categories()), status=200, mimetype='application/json')


@categories_bp.post("/create")
@RequiredKeys(body={'name', 'type', 'is_cumulative'})
def create_new_categorie():
    handle = s.CreateCategorie(logger=services.logger)
    return handle.execute()
