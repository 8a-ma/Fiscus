import pandas as pd
from services.factory import services


def get_all_categories() -> pd.DataFrame:
    query = services.db.read_sql_file('categories', 'get_all_categories.sql')

    return services.db.simple_query("get all categories", query)

def create_new_categorie(values: tuple) -> pd.DataFrame:
    query = services.db.read_sql_file('categories', 'create_new_categorie.sql')

    return services.db.insert_query("create new categorie", query, query_params=values)
