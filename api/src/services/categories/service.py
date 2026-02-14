from . import controller as c

def get_all_categories() -> dict:
    return c.get_all_categories().to_dict(orient='index',)
