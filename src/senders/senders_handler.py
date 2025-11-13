import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import constants
from config_parser import config
from logger_setup import logger
from caetra_exceptions import ConfigurationError
from dict_handler import validate_dict_structure
from send_canary_dns_token import send_canary
from send_telegram_message_to_chat import send_telegram


def check_send_config(senders_config):
    # check of any kind of config has senders
    # TODO: re-think this maybe we do not want to be mandatory
    if not senders_config.get("senders"):
        msgerr = "Any sender configured on general or shield"
        raise ConfigurationError(msgerr)

    # check that the sender config structure is correct
    is_enable = []
    for key, value in senders_config.get("senders").items():
        match key:
            case constants.CONFIG_SENDER_KEY_CANARYTOKENS:
                validate_dict_structure(
                    constants.CONFIG_SENDER_STRUCT_CANARYTOKENS,
                    value,
                    constants.CONFIG_SENDER_KEY_CANARYTOKENS,
                )
                is_enable.append(value["enable"])
            case constants.CONFIG_SENDER_KEY_TELEGRAM:
                validate_dict_structure(
                    constants.CONFIG_SENDER_STRUCT_TELEGRAM,
                    value,
                    constants.CONFIG_SENDER_KEY_TELEGRAM,
                )
                is_enable.append(value["enable"])
            case _:
                msgerr = f"Unknown sender configuration: '{key}'"
                raise ConfigurationError(msgerr)

    # check is any sender is enable, otherwise send an error
    if not any(is_enable):
        msgerr = "Any sender is enable"
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

    return senders_config.get("senders")


def send(data, shield_config=None):
    print("============")
    print(shield_config)
    print("============")
    senders_config = get_config(shield_config)
    for key, value in senders_config.items():
        match key:
            case constants.CONFIG_SENDER_KEY_CANARYTOKENS:
                if value["enable"]:
                    send_canary(
                        f"@{config['caetra']['machine']}: {data}", value["token"]
                    )

            case constants.CONFIG_SENDER_KEY_TELEGRAM:
                if value["enable"]:
                    send_telegram(
                        f"At {config['caetra']['machine']}: {data}",
                        value["bot_api_key"],
                        value["chat_id"],
                    )
