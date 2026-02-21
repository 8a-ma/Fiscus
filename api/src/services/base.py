import time
import json
import logging
from flask import request, Response
from abc import ABC, abstractmethod
from typing import Callable


class BaseEndpointAbstract(ABC):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

        self.raw_data = None
        self.start_time = None

    def execute(self) -> Response:
        try:
            response, status_code = self.handle_request()

        except ValueError as e:
            response, status_code = {"error": "Bad Request", "message": str(e)}, 400

        except Exception as e:
            response, status_code = {"error": "Internal Server Error", "message": str(e)}, 500

        finally:
            return Response(
                json.loads(response),
                status=status_code,
                mimetype='application/json'
            )

    @abstractmethod
    def handle_request(self) -> tuple[dict, int]:
        pass

    def _log_info(self, step: str) -> None:
        duration = time.time() - self.start_time

        if "X-Forwarded-For" in request.headers:
            client_ip = request.headers['X-Forwarded-For']

        else:
            client = request.remote_addr

        extra = {
            "duration_ms": round(duration * 1000, 2),
            "client_ip": client_ip,
            "class_name": self.__class__.__name__,
            "step": step
        }

        self.logger.info(f"[{extra.get('class_name')}] - {extra.get('stage')}, duration (ms): {extra.get('duration_ms')}, client_ip: {extra.get('client_ip')}", extra=extra)

    def _log_exception(self, step: str, exc: Exception) -> None:
        duration = time.time() - self.start_time

        if "X-Forwarded-For" in request.headers:
            client_ip = request.headers['X-Forwarded-For']

        else:
            client = request.remote_addr

        extra = {
            "duration_ms": round(duration * 1000, 2),
            "client_ip": client_ip,
            "class_name": self.__class__.__name__,
            "step": step,
            "error": str(exc)
        }

        self.logger.exception(f"[{extra.get('class_name')}] - {extra.get('stage')}, duration (ms): {extra.get('duration_ms')}, client_ip: {extra.get('client_ip')}, error: {extra.get('error')}", extra=extra)
