import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)s [%(levelname)s]: %(message)s",
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
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("caetra")
logger_shields = logging.getLogger("caetra_shields")
