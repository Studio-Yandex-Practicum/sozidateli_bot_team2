import os
from dataclasses import dataclass


@dataclass
class Settings:
    bot_token: str = os.getenv('BOT_TOKEN')
    throttle_time_spin: int = os.getenv('THROTTLE_TIME_SPIN')
    throttle_time_other: int = os.getenv('THROTTLE_TIME_OTHER')
    manager_chat_id: int = os.getenv('MANAGER_CHAT_ID')
    url: str = os.getenv('URL', 'http://localhost:8000')
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    webhook_path: str | None = os.getenv('WEBHOOK_PATH')
    webhook_uri: str | None = os.getenv('WEBHOOK_URI')
    web_server_host: str = os.getenv('WEB_SERVER_HOST', 'localhost')
    web_server_port: int | str = os.getenv('WEB_SERVER_PORT', 8000)
    is_pooling: bool = (True if os.getenv(
        'IS_POOLING'
    ) in ('true', '1', 'True') else False)
