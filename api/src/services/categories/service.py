import time
import json
from . import controller as c
from flask import request, Response
from services.base import BaseServicesAbstract


def get_all_categories() -> dict:
    return c.get_all_categories().to_dict(orient='index',)


class CreateCategorie(BaseServicesAbstract):
    def handle_request(self) -> Response:
        try:
            self.raw_data = requests.get_json()

            name, type, is_cumulative = self.raw_data.get('name', 'error'), self.raw_data.get('type', 'error'), self.raw_data.get('is_cumulative', False)

            id = c.create_new_categorie(tuple(name, type, is_cumulative))

            if isinstance(id, pd.DataFrame):
                id = id['id'].iloc[0]

            response = {
                "id": int(id)
            }

            status_code = 201

        except Exception as e:
            response = {
                "error": "Internal Server Error",
                "message": str(e)
            }

            status_code = 500

        finally:
            return Response(json.dumps(response), status=status_code, mimetype='application/json')
