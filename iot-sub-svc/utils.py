import json
import logging
from typing import Dict, Any

def setup_logging():
    cfg = Config()
    logging.basicConfig(
        level=cfg.log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(cfg.log_file),
            logging.StreamHandler()
        ]
    )

def validate_json(payload: str) -> bool:
    try:
        json.loads(payload)
        return True
    except json.JSONDecodeError:
        return False

def format_message_data(msg_data: Dict[str, Any]) -> str:
    return json.dumps(msg_data, indent=2, default=str)
