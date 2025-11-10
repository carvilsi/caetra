import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from config_parser import config
from logger_setup import logger
from caetra_exceptions import ConfigurationError

def send(message, shield_config=None):
    senders_config = None

    # read the general configuration
    if not shield_config:
        logger.debug("general config: " + str(config))
        senders_config = config
    # use the custom config comming from shields
    else:
        logger.debug("shield config: " + str(shield_config))
        senders_config = shield_config 
    
    # check of any kind of config has senders
    if not senders_config.get("senders"):
        msgerr = f"Any sender configured on general or shield"
        logger.warning(msgerr)
        raise ConfigurationError(msgerr)

