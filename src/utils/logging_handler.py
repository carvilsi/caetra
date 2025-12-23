from logger_setup import logger_shields, logger


def log_shield_exception(e, shield_name):
    logger.error(e)
    msg = "[!] " + shield_name.upper() + " " + str(e)
    logger_shields.error(msg)

def log_shield_exception_warn(e, shield_name):
    logger.warning(e)
    msg = "[!] " + shield_name.upper() + " " + str(e)
    logger_shields.warning(msg)
