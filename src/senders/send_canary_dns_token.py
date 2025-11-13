import base64
import socket
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils/"))

from logger_setup import logger

DOT = "."
MAGIC_STRING = "G69"
CANARY_PORT = 80
MAX_DNS_CHUNKS = 3


def call_dns_canary_token(canary_dns_call):
    try:
        socket.getaddrinfo(canary_dns_call, CANARY_PORT)
    except socket.gaierror as e:
        logger.error("there was a getaddrinfo error: ", e)
    except Exception as e:
        logger.error("there was another error: ", e)
    else:
        logger.debug(f"DNS Canary Token sent: {canary_dns_call}")


def get_dns_canary_token_call(data, canary_dns_token):
    canary_dns_call = None

    encoded_data = DOT.join(
        filter(
            lambda x: x,
            re.split(
                r"(.{63})",
                base64.b32encode(data.encode("utf8")).decode("utf8").replace("=", ""),
            ),
        )
    )

    spl = encoded_data.split(DOT)
    if len(spl) > MAX_DNS_CHUNKS:
        spl = spl[0:MAX_DNS_CHUNKS]

    canary_dns_call = DOT.join(spl) + DOT + DOT.join([MAGIC_STRING, canary_dns_token])

    return canary_dns_call


def send_canary(data, canary_dns_token):
    canary_dns_call = get_dns_canary_token_call(data, canary_dns_token)
    call_dns_canary_token(canary_dns_call)
