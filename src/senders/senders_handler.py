import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import constants
from config_parser import config
from logger_setup import logger
from caetra_exceptions import ConfigurationError
from dict_handler import validate_dict_structure

def check_send_config(senders_config):
    # check of any kind of config has senders
    # TODO: re-think this maybe we do not want to be mandatory
    if not senders_config.get("senders"):
        msgerr = f"Any sender configured on general or shield"
        raise ConfigurationError(msgerr)

def get_config(shield_config=None):
    senders_config = None

    # read the general configuration
    if not shield_config.get("senders"):
        logger.debug("general config: " + str(config))
        senders_config = config
    # use the custom config comming from shields
    else:
        logger.debug("shield config: " + str(shield_config))
        senders_config = shield_config
    
    check_send_config(senders_config)

    print(type(senders_config))
    for key, value in senders_config.get("senders").items():
        print("key: " + key)
        print("value: " + str(value))
        # TODO move this into a switch
        if key == constants.CONFIG_SENDER_KEY_CANARYTOKENS:
            # TODO: move this as a raise
            if validate_dict_structure(constants.CONFIG_SENDER_STRUCT_CANARYTOKENS, value):
        else if key == constants.CONFIG_SENDER_KEY_TELEGRAM:


    return senders_config

def send(message, shield_config=None):
    senders_config = get_config(shield_config) 
    
    
        
