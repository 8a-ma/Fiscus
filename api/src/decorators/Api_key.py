from flask import request, abort
from functools import wraps


class RequireAPIKey:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            api_key_header = request.headers.get('x-api-key')
            if api_key_header == self.api_key:
                return func(*args, **kwargs)

            abort(401, description="Invalid or missing API Key")

        return decorated_function
