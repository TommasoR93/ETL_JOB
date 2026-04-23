import logging
from pathlib import Path
from config.config import load_config

conf = load_config()
log_conf = conf.get("LOGGING", "").get("log_file", {})

def create_log():
    logger = logging.getLogger(__name__)

    #create path
    path = Path(__file__).resolve().parents[1]/log_conf

    #filehandler
    file_handler = logging.FileHandler(path)
    logger.addHandler(file_handler)

    #level
    level_str = conf.get("LOGGING", "").get("level", {})
    level = getattr(logging, level_str.upper(), logging.INFO)
    logger.setLevel(level )

    #formatter
    formatter = conf.get("LOGGING", {}).get("formatter", "")
    formatter_str = logging.Formatter(formatter)
    file_handler.setFormatter(formatter_str)
    
    return logger
