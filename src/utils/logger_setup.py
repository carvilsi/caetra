import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)s [%(levelname)s]: %(message)s",
        },
        "siem": {
            # fixed "caetra_siem:" prematch so a SIEM decoder can find the
            # JSON payload regardless of what the local syslog daemon
            # prepends (hostname, timestamp, pid, ...)
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
            "class": "logging.handlers.SysLogHandler",
            "formatter": "siem",
            # dedicated facility, kept separate from "logsys" above, so a
            # SIEM agent (e.g. Wazuh) can be pointed only at these
            # structured events instead of every human-readable log line
            "facility": "local0",
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
