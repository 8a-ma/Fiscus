import secrets
import logging
from flask import Flask, Response
from flask_wtf import CSRFProtect
from src.config.config import Config


app = Flask(__name__)
csrf = CSRFProtect()
logger = Config.get_logger(__name__) or logging.getLogger()

app.config.update(
    SECRET_KEY=secrets.token_hex(64)
)

@app.get('/health')
def health():
    return Response(status=204)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8000)

    finally:
        pass
