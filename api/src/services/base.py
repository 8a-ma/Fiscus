import time
import logging
from flask import request, Response
from abc import ABC, abstractmethod
from typing import Callable


class BaseServicesAbstract(ABC):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

        self.raw_data = None
        self.start_time = None

    @abstractmethod
    def handle_request(self) -> Response | Callable:
        pass

    def _log_info(self, step: str):
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

    def _log_exception(self, step: str, exc: Exception):
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
