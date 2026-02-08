import secrets
import logging
from flask import Flask, Response
from config.config import Config
from services.factory import services

app = Flask(__name__)
logger = Config.get_logger(__name__) or logging.getLogger()

app.config.update(
    SECRET_KEY=secrets.token_hex(64)
)

services.init_app(logger)

@app.get('/health')
def health():
    return Response(status=204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
