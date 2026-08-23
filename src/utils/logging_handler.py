import json
from datetime import datetime, timezone

from src.utils.logger_setup import logger_shields, logger, logger_siem
from src.utils.config_parser import config


def log_shield_exception(e, shield_name):
    logger.error(e)
    msg = "[!] " + shield_name.upper() + " " + str(e)
    logger_shields.error(msg)


def log_shield_exception_warn(e, shield_name):
    logger.warning(e)
    msg = "[!] " + shield_name.upper() + " " + str(e)
    logger_shields.warning(msg)


def log_shield_triggered(shield_name, message):
    logger_shields.warning(f"{shield_name} triggered: {message}")
    if config.get("caetra", {}).get("siem_logging_enabled", True):
        _log_siem_event(shield_name, "triggered", message)


def _log_siem_event(shield_name, state, message):
    # "status" is a reserved field name in Wazuh's rule engine, so this is
    # named "state" to stay decodable as a plain dynamic field
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "product": "caetra",
        "machine": config.get("caetra", {}).get("machine"),
        "shield": shield_name,
        "state": state,
        "message": message,
    }
    logger_siem.info(json.dumps(payload))
