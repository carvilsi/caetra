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

