import time
import json
import pandas as pd
from . import controller as c
from flask import request, Response
from services.base import BaseEndpointAbstract


def get_all_categories() -> dict:
    return c.get_all_categories().to_dict(orient='index',)


def verify_category_id(category_id: int) -> bool:
    categories_ids = get_all_categories()

    return any(cat.get('id') == category_id for cat in categories_ids.values())


class CreateCategorie(BaseEndpointAbstract):
    def handle_request(self) -> tuple[dict, int]:
        self.raw_data = request.get_json() or {}

        name = self.raw_data.get('name')
        category_type = self.raw_data.get('type')
        is_cumulative = self.raw_data.get('is_cumulative', False)

        if not name or not category_type:
            raise ValueError("Name and Type are required fields")

        result = c.create_new_categorie((name, category_type, is_cumulative))

        if isinstance(result, pd.DataFrame):
            if not result.empty:
                new_id = result['id'].iloc[0]
            else:
                raise Exception("No ID returned from database")
        else:
            new_id = result

        response = {"id": int(new_id)}
        status_code = 201

        return response, status_code
