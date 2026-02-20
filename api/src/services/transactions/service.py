import time
import json
import pandas as pd
from . import controller as c
from flask import request, Response
from services.base import BaseServicesAbstract
from services.categories.service import get_all_categories


class CreateTransaction(BaseServicesAbstract):
    def _verify_category_id(category_id: int) -> bool:
        categories_ids = get_all_categories()

        return any(cat.get('id') == category_id for cat in categories_ids.values())

    def handle_request(self) -> Response:
        try:
            self.raw_data = request.get_json() or {}

            category_id = self.raw_data.get('category_id')
            amount = self.raw_data.get('amount')
            description = self.raw_data.get('description')

            if not category_id or not amount:
                raise ValueError("Name and Type are required fields")

            if self._verify_category_id(category_id):
                raise ValueError(f"Category id ({category_id}) not exist")

            result = c.create_transaction((category_id, amount, description))

            if isinstance(result, pd.DataFrame):
                if not result.empty:
                    id = result['id'].iloc[0]

                else:
                    raise Exception("No ID returned from database")

            else:
                id = result

            response = {"id": int(id)}
            status_code = 201

        except ValueError as e:
            response = {"error": "Bad Request", "message": str(e)}
            status_code = 400

        except Exception as e:
            response = {"error": "Internal Server Error", "message": str(e)}
            status_code = 500

        finally:
            return Response(
                json.dumps(response),
                status=status_code,
                mimetype='application/json'
            )
