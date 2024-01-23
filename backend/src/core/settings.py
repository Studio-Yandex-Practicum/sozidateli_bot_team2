import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Настройки проекта."""

    db_url: str = os.getenv("DB_URL", "sqlite+aiosqlite:///sqlite.db")
    app_title: str = "API для админки проекта 'Созидатели'."
