import logging

from fastapi import FastAPI

from .translate import get_translation

app = FastAPI()
_logger = logging.getLogger("uvicorn.error")


@app.get("/translate")
def read_root(name: str, content: str, source: str, target: str):
    _logger.info(f"[Translator] [Server] [{name}] Content: {content}")
    translation = get_translation(content, source, target, name)
    _logger.info(f"[Translator] [Server] [{name}]  Translation: {translation}")
    return {"translation": translation or content}


@app.get("/log")
def log(name: str, content: str):
    _logger.info(f"[Translator] [Client] [{name}] {content}")
    return content
