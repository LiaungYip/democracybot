# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Uses Python 3.

import logging

from telegram.ext import (Updater, CommandHandler)

from edit_poll import cmd_set_title, cmd_set_url, cmd_set_target_chat, \
    cmd_activate, cmd_deactivate
from help import cmd_help, cmd_start
from misc_cmd import cmd_get_chat_id
from new_poll import cmd_new_poll
from poll_admin import cmd_list_polls, cmd_list_tokens
from vote import cmd_vote, vote_conversation_handler

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

    handlers = (
        ("newpoll", cmd_new_poll),
        ("getchatid", cmd_get_chat_id),
        ("settitle", cmd_set_title),
        ("settargetchat", cmd_set_target_chat),
        ("seturl", cmd_set_url),
        ("activate", cmd_activate),
        ("deactivate", cmd_deactivate),
        ("help", cmd_help),
        ("listpolls", cmd_list_polls),
        ("listtokens", cmd_list_tokens),
        ("start", cmd_start),
    )

    for h in handlers:
        dp.add_handler(CommandHandler(*h))

    # dp.add_handler(CommandHandler("vote", cmd_vote))
    dp.add_handler(vote_conversation_handler())
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
