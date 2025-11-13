#!/usr/bin/env python

import click

def prompt_canarytoken(ctx, param, canarytoken_sender):
    if canarytoken_sender:
        token = ctx.params.get('canarytoken')
        if not token:
            token = click.prompt('Canary DNS token')

        return token


def prompt_telegram(ctx, param, telegram_sender):
    if telegram_sender:
        chatid = ctx.params.get('telegram_chat_id')
        if not chatid:
            chatid = click.prompt('Telegram chat_id', type=click.INT)

        botapikey = ctx.params.get('telegram_bot_api_key')
        if not botapikey:
            botapikey = click.prompt('Telegram bot_api_key', type=click.STRING)

        return (chatid, botapikey) 


@click.command()
@click.option("--shield-name", type=click.STRING, required=True, prompt="Shield name", help="New caetra shield name.")
@click.option("--shield-description", type=click.STRING, required=False, prompt="Shield description", default="None", help="Write down about what this Shield does.")
@click.option("--kprobe-event", type=click.STRING, required=True, prompt="Kprobe event", help="Kprobe event.")
@click.option("--c-function-name", type=click.STRING, required=True, prompt="Function name", help="Name function for c code.")
@click.option("--kheaders-include", type=click.STRING, required=True, prompt="Linux header to include", help="Linux header to includ on kernel c code, e.g. 'linux/usb.h'")
@click.option("--kstrct", type=click.STRING, required=True, prompt="Related kprobe related struct to get data", help="Linux struct to retrieve data, e.g. 'usb_device'")
@click.option("--shield-enable", type=click.BOOL, required=True, default="y", prompt="Is this Shield enabled?", help="If this Shield will be enabled or not")
@click.option("--shield-feature", type=click.STRING, required=False, default="None", prompt="Name of the feature if is has one", help="Will be the feature variable for the Shield.")
@click.option('--canarytoken-sender', prompt="Should this Shield send notifications with Cananry tokens?", is_flag=True, default=True, callback=prompt_canarytoken)
@click.option('--canarytoken', is_eager=True, type=click.STRING)
@click.option('--telegram-sender', prompt="Should this Shield send notifications with Telegram Bot?", is_flag=True, default=True, callback=prompt_telegram)
@click.option('--telegram-chat-id', is_eager=True)
@click.option('--telegram-bot-api-key', is_eager=True)


def cli(shield_name, shield_description, kprobe_event, c_function_name, kheaders_include, kstrct, shield_enable, shield_feature, canarytoken_sender, canarytoken, telegram_sender, telegram_chat_id, telegram_bot_api_key):
    shield_name = shield_name.replace(" ", "_")
    c_function_name = c_function_name.replace(" ", "_")
    
    if canarytoken_sender:
        canarytoken = canarytoken_sender
        canarytoken_sender = True
    
    if telegram_sender:
        telegram_chat_id = telegram_sender[0]
        telegram_bot_api_key = telegram_sender[1]
        telegram_sender = True

    print(f"shield_name: {shield_name}")
    print(f"shield_description: {shield_description}")
    print(f"kprobe_event: {kprobe_event}")
    print(f"c_function_name: {c_function_name}")
    print(f"kheaders_include: {kheaders_include}")
    print(f"kstrct: {kstrct}")
    print(f"shield_enable: {shield_enable}")
    print(f"shield_feature: {shield_feature}")
    print(f"canarytoken_sender: {canarytoken_sender}")
    print(f"canarytoken: {canarytoken}")
    print(f"telegram_sender: {telegram_sender}")
    print(f"telegram_chat_id: {telegram_chat_id}")
    print(f"telegram_bot_api_key: {telegram_bot_api_key}")

if __name__ == '__main__':
    cli()



