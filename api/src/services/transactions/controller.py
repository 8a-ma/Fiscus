import pandas as pd
from services.factory import services


def create_new_transaction(values: tuple) -> pd.DataFrame:
    query = services.db.read_sql_file('transactions', 'create_transaction.sql')

    return services.db.insert_query('create new transactions', query, query_params=values)


def get_transactions_filtered(filters: dict) -> pd.DataFrame:
    query = services.db.read_sql_file("transactions", "get_transactions.sql")
    params = []

    if category_id := filters.get('category_id'):
        query += " and category_id = %s"
        params.append(category_id)

    if month := filters.get('month'):
        query += " and extract(month from created_at) = %s"
        params.append(month)

    if year := filters.get('year'):
        query += " and extract(year from created_at) = %s"
        params.append(year)

    allowed_columns = ["created_at", "amount", "category_id"]
    sort_columns = sort_by if sort_by := filters.get('sort_by') in allowed_columns else "created_at"

    order_by = "DESC" if f["order"].upper() == "DESC" else "ASC"

    query += f" order by {sort_columns} {order_by}"

    query += " limit %s offset %s;"
    params.extend([filters.get('limit'), filters.get('offset')])

    return services.db.read_sql_file("get transactions", query, query_params=tuple(params))
