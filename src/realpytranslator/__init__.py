import uvicorn

from .model import Settings
from .server import app

_settings = Settings()


def serve():
    uvicorn.run(app, host=str(_settings.server.host), port=_settings.server.port)
