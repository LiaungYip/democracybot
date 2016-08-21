# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Uses Python 3.

import logging

from telegram.ext import (Updater, CommandHandler)

from edit_poll import cmd_set_title, cmd_set_url, cmd_set_target_chat, \
    cmd_activate, cmd_deactivate
from misc_cmd import cmd_get_chat_id
from new_poll import cmd_new_poll

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def getToken():
    with open("telegram-bot-api-token.txt") as fh:
        token = fh.read().strip()
    return token


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(getToken())

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("newpoll", cmd_new_poll))
    dp.add_handler(CommandHandler("getchatid", cmd_get_chat_id))
    dp.add_handler(CommandHandler("settitle", cmd_set_title))
    dp.add_handler(CommandHandler("settargetchat", cmd_set_target_chat))
    dp.add_handler(CommandHandler("seturl", cmd_set_url))
    dp.add_handler(CommandHandler("activate", cmd_activate))
    dp.add_handler(CommandHandler("deactivate", cmd_deactivate))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
