import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    """Настройки проекта."""

    db_url: str = os.getenv("DB_URL", "sqlite+aiosqlite:///sqlite.db")
    app_title = "API для проекта 'Созидатели'."
    admin_panel_user = os.getenv("ADMIN_PANEL_USER")
    admin_panel_password = os.getenv("ADMIN_PANEL_PASSWORD")
