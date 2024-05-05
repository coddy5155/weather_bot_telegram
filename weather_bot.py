#!/usr/bin/python

import requests
import re
import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

def get_taf_met(str):

    taf = re.findall("TAF:<\/b>[\S\n ]*?(?=<\/p>)", str)
    met = re.findall("METAR:<\/b>[\S\n ]*?(?=<\/p>)", str)
    taf2 = taf[0].replace("</b>", "")
    met2 = met[0].replace("</b>", "")

    respond = taf2 + "\n\r" + met2
    return respond

def get_weather(name):

    payload = { 'icao': name.upper() }

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36 '}

    r = requests.get('https://ru.allmetsat.com/metar-taf/russia.php', params=payload, headers=headers)

    stp = get_taf_met(r.text)

    logger.info("Response: %s", stp)

    return stp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = update.effective_user

    EnterText = a = "Hello, dear friend!" +"\n"+ "To get weather information just type ICAO designator of airdrome."+"\n"+ "Example: uuee"

    await update.message.reply_text(EnterText)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text:
        # Reply to the message
        user = update.effective_user

        logger.info("Found message! user %s - %s - \"%s\"", user.id, user.name, update.message.text)

    await update.message.reply_text( get_weather(update.message.text) )

logger = logging.getLogger()
logging.basicConfig( format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO )
fh = logging.FileHandler('weather.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger.addHandler(fh)

def main() -> None:

    application = Application.builder().token("TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":

    main()

