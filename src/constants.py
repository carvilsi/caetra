SHIELD_PATH = "./src/shields/"
SHIELD_DEPLOYING_SCRIPT = "deploying.py"
SHIELD_CONFIG_EXT = ".toml"

CAETRA_SENDER_LABEL = "Shield"

CONFIG_SENDER_KEY_TELEGRAM = "telegram"
CONFIG_SENDER_STRUCT_TELEGRAM = {
    "enable": bool,
    "chat_id": int,
    "bot_api_key": str,
}

CONFIG_SENDER_KEY_CANARYTOKENS = "canarytokens"
CONFIG_SENDER_STRUCT_CANARYTOKENS = {
    "enable": bool,
    "token": str,
}

CONFIG_SHIELD_MANDATORY = {
    "enable": bool,
    "action_label": str,
}

MAX_ACTIONS_TO_SEND = 3
COOL_DOWN_TIME_TO_SEND = 10 # seconds
NS_TO_S = 1000000000

HID_ADD_ACT = 0
HID_REMOVE_ACT = 1


