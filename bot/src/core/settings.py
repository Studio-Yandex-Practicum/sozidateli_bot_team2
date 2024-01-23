import os
from dataclasses import dataclass


@dataclass
class Settings:
    bot_token: str = os.getenv('BOT_TOKEN')
    throttle_time_spin: int = os.getenv('THROTTLE_TIME_SPIN')
    throttle_time_other: int = os.getenv('THROTTLE_TIME_OTHER')
    url: str = os.getenv('URL', 'http://localhost:8000')
