import sqlite3

from openai import OpenAI

from .model import Settings

DATABASE_COLUMNS = "(source text, language text, translation text)"

_settings = Settings()
_openai_client = OpenAI(
    base_url=str(_settings.llm.base_url), api_key=_settings.llm.api_key
)
_db_connection = sqlite3.connect(
    _settings.translate.persistence, check_same_thread=False
)
_cursor = _db_connection.cursor()

# initialize persistence db
_cursor.execute("create table if not exists '_default' " + DATABASE_COLUMNS)


def get_from_persistence(language: str, content: str, name: str = "_default") -> str:
    _cursor.execute(f"create table if not exists '{name}' {DATABASE_COLUMNS}")
    _db_connection.commit()

    if result := _cursor.execute(
        f"select translation from '{name}' where source = ? and language = ?",
        (content, language),
    ).fetchone():
        return result[0]

    if result := _cursor.execute(
        "select translation from _default where source = ? and language = ?",
        (content, language),
    ).fetchone():
        return result[0]

    return ""


def store_to_persistence(
    language: str, content: str, translation: str, name: str = "_default"
):
    _cursor.execute(f"create table if not exists '{name}' {DATABASE_COLUMNS}")
    _cursor.execute(
        f"insert into '{name}' values (?, ?, ?)", (content, language, translation)
    )
    _db_connection.commit()


def get_translation(
    content: str, source_language: str, target_language: str, name: str = "_default"
) -> str:
    if result := get_from_persistence(target_language, content, name):
        return result

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
            {"role": "user", "content": content},
        ],
        stream=False,
    )

    translation = completion.choices[0].message.content
    if translation:
        store_to_persistence(target_language, content, translation, name)
        return translation
    return ""
