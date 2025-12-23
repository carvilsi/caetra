import requests

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils"))
from logger_setup import logger

HEADERS = {"Content-Type": "application/json"}


def send_telegram(data, bot_api_key, chat_id):
    try:
        url = f"https://api.telegram.org/bot{bot_api_key}/sendMessage"

        data = {"chat_id": f"{chat_id}", "text": data}

        logger.debug("Telegram to send url: " + url + " with data: " + str(data))

        response = requests.post(url, headers=HEADERS, json=data)

        logger.debug("Telegram Status Code: " + str(response.status_code))
        logger.debug("Telegram Response: " + str(response.json()))

    except requests.exceptions.HTTPError as errh:
        logger.error("Telegram Error HTTP: " + str(errh))
    except requests.exceptions.RequestException as errex:
        logger.error("Telegram Error Request: " + str(errex))
    except Exception as e:
        logger.error("Telegram Error: " + str(e))
