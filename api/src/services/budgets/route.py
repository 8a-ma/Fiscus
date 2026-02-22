from . import service as s
from flask import Blueprint
from services.factory import services
from decorators.Keys_required import RequiredKeys


budgets_bp = Blueprint('budgets', __name__, url_prefix='/v1/budgets')
params = {
    "logger": services.logger
}


@budgets_bp.get("")
def get_budgets():
    handle = s.GetBudgets(**params)
    return handle.execute()


@budgets_bp.post("/create")
@RequiredKeys(body={'category_id', 'amount'})
def create_budget():
    handle = s.CreateBudget(**params)
    return handle.execute()


@budgets_bp.put("/update")
@RequiredKeys(body={'id', 'category_id', 'amount'})
def update_budget():
    handle = s.UpdateBudget(**params)
    return handle.execute()


@budgets_bp.delete("/delete")
@RequiredKeys(body={'id'})
def delete_budget():
    handle = s.DeleteBudget(**params)
    return handle.execute()
