import pandas as pd
from services.factory import services


def create_new_transaction(values: tuple) -> pd.DataFrame:
    query = services.db.read_sql_file('transactions', 'create_transaction.sql')

    return services.db.insert_query('create new transactions', query, query_params=values)
