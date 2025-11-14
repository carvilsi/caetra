#!/usr/bin/env python

import click
import os
from jinja2 import Environment, FileSystemLoader

FOLDER_TEMPLATE = "templates"
OUTPUT_TEMPLATE = "generator-output"
C_TEMPLATE = "ctr_bpf_c.jinja"
PYTHON_TEMPLATE = "ctr_bpf_py.jinja"
TOML_TEMPLATE = "ctr_bpf_toml.jinja"


def write_template_output(shield_name, file_extension, content):
    with open(
        f"{OUTPUT_TEMPLATE}/{shield_name}/{shield_name}.{file_extension}", "w", encoding="utf-8"
    ) as f:
        f.write(content)


def prompt_canarytoken(ctx, param, canarytoken_sender):
    if canarytoken_sender:
        token = ctx.params.get("canarytoken")
        if not token:
            token = click.prompt("Canary DNS token")

        return token


def prompt_telegram(ctx, param, telegram_sender):
    if telegram_sender:
        chatid = ctx.params.get("telegram_chat_id")
        if not chatid:
            chatid = click.prompt("Telegram chat_id", type=click.INT)

        botapikey = ctx.params.get("telegram_bot_api_key")
        if not botapikey:
            botapikey = click.prompt("Telegram bot_api_key", type=click.STRING)

        return (chatid, botapikey)


@click.command()
@click.option(
    "--shield-name",
    type=click.STRING,
    required=True,
    prompt="Shield name",
    help="New caetra shield name.",
)
@click.option(
    "--shield-description",
    type=click.STRING,
    required=False,
    prompt="Shield description",
    default="None",
    help="Write down about what this Shield does.",
)
@click.option(
    "--kprobe-event",
    type=click.STRING,
    required=True,
    prompt="Kprobe event",
    help="Kprobe event.",
)
@click.option(
    "--kheaders-include",
    type=click.STRING,
    required=True,
    prompt="Linux header to include",
    help="Linux header to includ on kernel c code, e.g. 'linux/usb.h'",
)
@click.option(
    "--kstrct",
    type=click.STRING,
    required=True,
    prompt="Related kprobe related struct to get data",
    help="Linux struct to retrieve data, e.g. 'usb_device'",
)
@click.option(
    "--shield-enable",
    type=click.BOOL,
    required=True,
    default="y",
    prompt="Is this Shield enabled?",
    help="If this Shield will be enabled or not",
)
@click.option(
    "--shield-feature",
    type=click.STRING,
    required=False,
    default="None",
    prompt="Name of the feature if is has one",
    help="Will be the feature variable for the Shield.",
)
@click.option(
    "--action-label",
    type=click.STRING,
    required=True,
    prompt="Action label",
    help="The label that describes the physical interaction, e.g. 'usb attached'",
)
@click.option(
    "--canarytoken-sender",
    prompt="Should this Shield send notifications with Cananry tokens?",
    is_flag=True,
    default=True,
    callback=prompt_canarytoken,
)
@click.option("--canarytoken", is_eager=True, type=click.STRING)
@click.option(
    "--telegram-sender",
    prompt="Should this Shield send notifications with Telegram Bot?",
    is_flag=True,
    default=True,
    callback=prompt_telegram,
)
@click.option("--telegram-chat-id", is_eager=True)
@click.option("--telegram-bot-api-key", is_eager=True)

def caetra_shield_generator(
    shield_name,
    shield_description,
    kprobe_event,
    kheaders_include,
    kstrct,
    shield_enable,
    shield_feature,
    action_label,
    canarytoken_sender,
    canarytoken,
    telegram_sender,
    telegram_chat_id,
    telegram_bot_api_key,
):
    shield_name = shield_name.replace(" ", "_")

    if canarytoken_sender:
        canarytoken = canarytoken_sender
        canarytoken_sender = "true" 
    else:
        canarytoken_sender = None

    if telegram_sender:
        telegram_chat_id = telegram_sender[0]
        telegram_bot_api_key = telegram_sender[1]
        telegram_sender = "true" 
    else:
        telegram_sender = None

    if shield_feature == "None":
        shield_feature = None
    else:
        shield_feature = shield_feature.replace(" ", "_")

    if shield_enable:
        shield_enable = "true"
    else:
        shield_enable = "false"

    if shield_description == "None":
        shield_description = None

    print(f"shield_name: {shield_name}")
    print(f"shield_description: {shield_description}")
    print(f"kprobe_event: {kprobe_event}")
    print(f"kheaders_include: {kheaders_include}")
    print(f"kstrct: {kstrct}")
    print(f"shield_enable: {shield_enable}")
    print(f"shield_feature: {shield_feature}")
    print(f"canarytoken_sender: {canarytoken_sender}")
    print(f"canarytoken: {canarytoken}")
    print(f"telegram_sender: {telegram_sender}")
    print(f"telegram_chat_id: {telegram_chat_id}")
    print(f"telegram_bot_api_key: {telegram_bot_api_key}")

    if not os.path.exists(f"{OUTPUT_TEMPLATE}"):
        os.makedirs(OUTPUT_TEMPLATE)

    if not os.path.exists(f"{OUTPUT_TEMPLATE}/{shield_name}"):
        os.makedirs(f"{OUTPUT_TEMPLATE}/{shield_name}")

    env = Environment(loader=FileSystemLoader(FOLDER_TEMPLATE))

    # Python Template
    python_template = env.get_template(PYTHON_TEMPLATE)
    python_output = python_template.render(
        shield_name=shield_name,
        kprobe_event=kprobe_event,
        shield_feature=shield_feature,
    )
    write_template_output(shield_name, "py", python_output)

    # C Kernel side Template
    c_template = env.get_template(C_TEMPLATE)
    c_output = c_template.render(
            shield_name=shield_name,
            kheaders_include=kheaders_include,
            kstrct=kstrct
    )
    write_template_output(shield_name, "c", c_output)

    # Toml Template
    toml_template = env.get_template(TOML_TEMPLATE)
    toml_output = toml_template.render(
            shield_name=shield_name,
            shield_description=shield_description,
            shield_enable=shield_enable,
            shield_feature=shield_feature,
            canarytoken_sender=canarytoken_sender,
            canarytoken=canarytoken,
            telegram_sender=telegram_sender,
            telegram_chat_id=telegram_chat_id,
            telegram_bot_api_key=telegram_bot_api_key,
            action_label=action_label
    )
    write_template_output(shield_name, "toml", toml_output)


if __name__ == "__main__":
    caetra_shield_generator()
