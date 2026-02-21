import time
import json
import pandas as pd
from . import controller as c
from flask import request, Response
from services.base import BaseServicesAbstract


def get_all_categories() -> dict:
    return c.get_all_categories().to_dict(orient='index',)


def verify_category_id(category_id: int) -> bool:
    categories_ids = get_all_categories()

    return any(cat.get('id') == category_id for cat in categories_ids.values())


class CreateCategorie(BaseServicesAbstract):
    def handle_request(self) -> Response:
        try:
            # 1. Obtener datos con valores por defecto seguros
            self.raw_data = request.get_json() or {}

            name = self.raw_data.get('name')
            category_type = self.raw_data.get('type')  # Evitamos 'type' porque es palabra reservada
            is_cumulative = self.raw_data.get('is_cumulative', False)

            # Validar campos obligatorios antes de ir a la DB
            if not name or not category_type:
                raise ValueError("Name and Type are required fields")

            # 2. Corregir sintaxis de tupla: tuple() recibe un iterable (lista/tupla)
            # Pasamos los datos al método de creación
            result = c.create_new_categorie((name, category_type, is_cumulative))

            # 3. Procesar el resultado (DataFrame o valor directo)
            if isinstance(result, pd.DataFrame):
                if not result.empty:
                    new_id = result['id'].iloc[0]
                else:
                    raise Exception("No ID returned from database")
            else:
                new_id = result

            response = {"id": int(new_id)}
            status_code = 201

        except ValueError as e:
            # Error de validación del cliente
            response = {"error": "Bad Request", "message": str(e)}
            status_code = 400

        except Exception as e:
            # Error de servidor o base de datos
            response = {"error": "Internal Server Error", "message": str(e)}
            status_code = 500

        finally:
            return Response(
                json.dumps(response),
                status=status_code,
                mimetype='application/json'
            )
