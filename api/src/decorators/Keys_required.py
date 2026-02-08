from flask import request, abort
from functools import wraps


class RequiredKeys:
    def __init__(self, args: set = set(), body: set = set()) -> None:
        self.args_required = args
        self.body_required = body

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            query_args = request.args.keys()
            missing_args = self.args_required - set(query_args)

            missing_body = set()

            if self.body_required:
                body_data = request.get_json(silent=True) or {}
                missing_body = self.body_required - set(body_data.keys())

            if missing_args or missing_body:
                abort(400, description="Bad Request")

            try:
                return func(*args, **kwargs)

            except Exception:
                abort(500, description="Internal Server Error")

        return decorated_function
