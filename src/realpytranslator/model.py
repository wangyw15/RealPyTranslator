from typing import Annotated

from ipaddress import IPv4Address
from pydantic import (
    AfterValidator,
    BaseModel,
    IPvAnyAddress,
    HttpUrl,
)
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


def _port_validator(value: int) -> int:
    if 0 < value < 65535:
        return value
    raise ValueError(f"Port number {value} is not between 0 and 65535")


class ServerModel(BaseModel):
    host: IPvAnyAddress = IPv4Address("127.0.0.1")
    port: Annotated[int, AfterValidator(_port_validator)] = 8080


class LLMModel(BaseModel):
    base_url: HttpUrl = HttpUrl("http://localhost:11434/v1")
    api_key: str = ""
    model: str = "qwen3:latest"
    prompt: str = "你是一名专业的翻译家，你的任务是把{source_language}文本翻译成{target_language}，逐行翻译，不要合并，原始保留文本中序号、标记符、占位符、换行符、转义符、代码调用过程等特殊内容，保持原来的格式。"


class Settings(BaseSettings):
    server: ServerModel = ServerModel()
    llm: LLMModel = LLMModel()

    model_config = SettingsConfigDict(
        env_prefix="realpy_translator_", toml_file="config.toml"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)
