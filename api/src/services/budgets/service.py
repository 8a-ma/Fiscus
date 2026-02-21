import time
import json
import pandas as pd
from . import controller as c
from flask import request, Response
from services.base import BaseEndpointAbstract
from services.categories.service import verify_category_id


class GetBudgets(BaseEndpointAbstract):
    def handle_request(self) -> tuple[dict, int]:
        params = request.args.to_dict()
        filters = {
            "category_id": params.get('category_id'),
            "month": params.get('month'),
            "year": params.get('year'),
            "limit": int(params.get('limit', 20)),
            "offest": int(params.get('offest', 0)),
            "sort_by": params.get("sort_by", "created_at"),
            "order": params.get('order', 'DESC')
        }

        df = c.get_budgets_filtered(filters)

        if df.empty:
            raise ValueError("Empty")

        response = {
            "data": df.to_dict(orient='records')
        }
        status_code = 200

        return response, status_code

class CreateBudget(BaseEndpointAbstract):
    def handle_request(self) -> tuple[dict, int]:
        self.raw_data = request.get_json() or {}

        category_id = self.raw_data.get('category_id')
        amount = self.raw_data.get('amount')

        if not category_id or not amount:
            raise ValueError("Category id and amount are required fields")

        if verify_category_id(category_id):
            raise ValueError(f"Category id ({category_id}) not exist")

        result = c.create_budget(tuple(category_id, amount,))

        if isinstance(result, pd.DataFrame):
            if not result.empty:
                id = result['id'].iloc[0]

            else:
                raise Exception("No ID returned from database")

        else:
            id = result

        response = {"id": int(new_id)}
        status_code = 201

        return response, status_code

class UpdateBudget(BaseServicesAbstract):
    def handle_request(self) -> tuple[dict, int]:
        self.raw_data = request.get_json() or {}

        id = self.raw_data.get('id')
        category_id = self.raw_data.get('category_id')
        amount = self.raw_data.get('amount')

        if not category_id or not amount:
            raise ValueError("Category id and amount are required fields")

        if verify_category_id(category_id):
            raise ValueError(f"Category id ({category_id}) not exist")

        result = ...

        response = ...
        status_code = 200

        return response, status_code


class DeleteBudget(BaseServicesAbstract):
    def handle_request(self) -> tuple[dict, int]:
        pass
