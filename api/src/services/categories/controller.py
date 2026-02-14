import pandas as pd
from services.factory import services


def get_all_categories() -> pd.DataFrame:
    query = services.db.read_sql_file('categories', 'get_all_categories.sql')

    return services.db.simple_query("get all categories", query)
