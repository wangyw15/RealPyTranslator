import logging

from fastapi import FastAPI
from openai import OpenAI

from .model import Settings

app = FastAPI()
_logger = logging.getLogger("uvicorn.error")
_settings = Settings()
_openai_client = OpenAI(
    base_url=str(_settings.llm.base_url), api_key=_settings.llm.api_key
)


def get_translation(content: str, source_language: str, target_language: str) -> str:
    completion = _openai_client.chat.completions.create(
        model=_settings.llm.model,
        messages=[
            {
                "role": "system",
                "content": _settings.llm.prompt.format(
                    source_language=source_language,
                    target_language=target_language,
                ),
            },
            {"role": "user", "content": "将下面的英文文本翻译成中文：" + content},
        ],
        stream=False,
    )
    return completion.choices[0].message.content or ""


@app.get("/translate")
def read_root(content: str, source: str, target: str):
    _logger.info(f"[Translator] [Server] Content: {content}")
    translation = get_translation(content, source, target)
    _logger.info(f"[Translator] [Server] Translation: {translation}" )
    return { "translation": translation or content}


@app.get("/log")
def log(content: str):
    _logger.info(f"[Translator] [Client] {content}")
    return content
