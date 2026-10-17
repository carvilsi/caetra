import logging
import logging.config
import socket

from src.utils.config_parser import config

SIEM_DEFAULT_HOST = "127.0.0.1"
SIEM_DEFAULT_PORT = 514


class UDPHandler(logging.Handler):
    """Sends each record as a plain-text UDP datagram.

    logging.handlers.DatagramHandler pickles records, which a syslog
    listener (e.g. Wazuh remoted) can't decode.
    """

    def __init__(self, host, port):
        super().__init__()
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def emit(self, record):
        try:
            self.socket.sendto(self.format(record).encode(), self.address)
        except Exception:
            self.handleError(record)

    def close(self):
        self.socket.close()
        super().close()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)s [%(levelname)s]: %(message)s",
        },
        "siem": {
            # fixed "caetra_siem:" prematch so the SIEM decoder can find the
            # JSON payload (see devops/wazuh/config/local_decoder.xml)
            "format": "caetra_siem: %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "./logs/caetra.log",
            "when": "d",
            "formatter": "default",
        },
        "stdout": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "logsys": {
            "level": "WARNING",
            "class": "logging.handlers.SysLogHandler",
            "formatter": "default",
            "facility": "syslog",
            "address": "/dev/log",
        },
        "logsiem": {
            "level": "INFO",
            "()": UDPHandler,
            "formatter": "siem",
            "host": config.get("caetra", {}).get("siem_host", SIEM_DEFAULT_HOST),
            "port": config.get("caetra", {}).get("siem_port", SIEM_DEFAULT_PORT),
        },
    },
    "loggers": {
        "caetra": {
            "handlers": ["file", "stdout"],
            "level": "DEBUG",
            "propagate": True,
        },
        "caetra_shields": {
            "handlers": ["file", "stdout", "logsys"],
            "level": "DEBUG",
            "propagate": True,
        },
        "caetra_siem": {
            "handlers": ["logsiem"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("caetra")
logger_shields = logging.getLogger("caetra_shields")
logger_siem = logging.getLogger("caetra_siem")
