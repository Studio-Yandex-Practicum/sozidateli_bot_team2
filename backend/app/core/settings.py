import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    """Настройки проекта."""

    db_url: str = os.getenv("DB_URL", "sqlite+aiosqlite:///sqlite.db")
    app_title = "API для проекта 'Созидатели'."
    admin_panel_user = os.getenv("ADMIN_PANEL_USER", "admin")
    admin_panel_password = os.getenv("ADMIN_PANEL_PASSWORD", "password")
    admin_middleware_secret = os.getenv(
        "ADMIN_MIDDLEWARE_SECRET", "1234567890"
    )
    users = {
        "admin": {
            "name": "SuperAdmin",
            "roles": [
                "read",
                "create",
                "edit",
                "delete",
                "action_make_published",
            ],
        },
    }
