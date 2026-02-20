import json
from . import service as s
from services.factory import services
from flask import Blueprint, abort, Response
from decorators.Keys_required import RequiredKeys


transactions_bp = Blueprint('transactions', __name__, url_prefix='/v1/transactions')


@transactions_bp.get("")
def list_transactions():
    return Response(status=204)


@transactions_bp.post("/create")
@RequiredKeys(body={"category_id", "amount"})
def create_transaction():
    handle = s.CreateTransaction(logger=services.logger)
    return handle.handle_request()
