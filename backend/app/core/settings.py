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
    secret = os.getenv("SECRET", "thesecretkey")
    first_superuser_email = os.getenv("FIRST_SUPERUSER_EMAIL")
    first_superuser_password = os.getenv("FIRST_SUPERUSER_PASSWORD")
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
