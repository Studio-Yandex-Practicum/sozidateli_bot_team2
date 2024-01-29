import logging
from pathlib import Path
from logging.handlers import StreamHandler, RotatingFileHandler
import sys

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


log_dir = __name__
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'bot.log'
logger_1 = logging.getLogger(__name__)
logger_2 = logging.getLogger(__name__)
logger_1.setLevel(logging.INFO)
logger_2.setLevel(logging.ERROR)
handler_1 = StreamHandler(sys.stdout)
handler_2 = RotatingFileHandler(log_file, maxBytes=10 ** 6, backupCount=5)
formatter = logging.Formatter(LOG_FORMAT, DT_FORMAT)
handler_1.setFormatter(formatter)
handler_2.setFormatter(formatter)
logger_1.addHandler(handler_1)
logger_2.addHandler(handler_2)
#def configure_logging(path: Path):
#    log_dir = path
#    log_dir.mkdir(exist_ok=True)
#    log_file = log_dir / 'bot.log'
#    rotating_file_handler = RotatingFileHandler(
#        log_file, maxBytes=10 ** 6, backupCount=5,
#    )
#    logging.basicConfig(
#        datefmt=DT_FORMAT,
#        format=LOG_FORMAT,
#        level=logging.INFO,
#        handlers=(rotating_file_handler, logging.StreamHandler()),
#    )
