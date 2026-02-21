import time
import json
import pandas as pd
from . import controller as c
from flask import request, Response
from services.base import BaseServicesAbstract
from services.categories.service import verify_category_id


class GetBudgets(BaseServicesAbstract):
    def handle_request(self) -> Response:
        try:
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

            response = {
                "data": df.to_dict(orient='records')
            }
            status_code = 200

        except Exception as e:
            response = {"error": "Internal Server Error", "message": str(e)}
            status_code = 500

        finally:
            return Response(
                json.dumps(response),
                status=status_code,
                mimetype='application/json'
            )


class CreateBudget(BaseServicesAbstract):
    def handle_request(self) -> Response:
        try:
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

        except ValueError as e:
            response = {"error": "Bad Request", "message": str(e)}
            status_code = 400

        except Exception as e:
            response = {"error": "Internal Server Error", "message": str(e)}
            status_code = 500

        finally:
            return Response(
                json.loads(response),
                status=status_code,
                mimetype='application/json'
            )


class UpdateBudget(BaseServicesAbstract):
    def handle_request(self) -> Response:
        try:
            self.raw_data = request.get_json() or {}

            id = self.raw_data.get('id')
            category_id = self.raw_data.get('category_id')
            amount = self.raw_data.get('amount')

            if not category_id or not amount:
                raise ValueError("Category id and amount are required fields")

            if verify_category_id(category_id):
                raise ValueError(f"Category id ({category_id}) not exist")

            result = ...

        except ValueError as e:
            response = {"error": "Bad Request", "message": str(e)}
            status_code = 400

        except Exception as e:
            response = {"error": "Internal Server Error", "message": str(e)}
            status_code = 500

        finally:
            return Response(
                json.loads(response),
                status=status_code,
                mimetype='application/json'
            )


class DeleteBudget(BaseServicesAbstract):
    def handle_request(self) -> Response:
        try:
            pass

        except ValueError as e:
            pass

        except Exception as e:
            pass

        finally:
            pass
