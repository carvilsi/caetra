import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'caetra': {
            'format': '%(asctime)s %(name)s [%(levelname)s]: %(message)s',
        },
        'caetra_shields': {
            'format': '%(name)s [%(levelname)s]: %(message)s',
        },
    },
    'handlers': {
        'file_caetra': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './logs/caetra.log',
            'formatter': 'caetra',
        },
        'stdout_caetra': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'caetra',
        },
        'syslog_caetra': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'caetra_shields',
            'facility': 'syslog',
        },
    },
    'loggers': {
        'caetra': {
            'handlers': ['file_caetra', 'stdout_caetra'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'shileds': {
            'handlers': ['file_caetra', 'stdout_caetra', 'syslog_caetra'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('caetra')
logger_shields = logging.getLogger('shields')
