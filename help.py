from text import text_private_chat_only

text_start = """Welcome to Democracy Bot!
This bot helps Telegram communities run anonymous polls.

To vote, just click /vote .

To make polls, see /help .
"""

text_help = """Welcome to Democracy Bot!
This bot helps Telegram communities run anonymous polls.

How to use:

To vote in an existing poll, click /vote .

How to make a new poll:

1. Add the bot to your chat group, i.e. "Telegram Users United".
2. In the group "Telegram Users United", type /getchatid
3. The bot should respond with:

> The Chat ID for this chat is:
> -1234567890123

4. In private message with the bot, type /newpoll and follow the prompts.

Commands available:

/vote - Get a token to vote in an existing poll.
/newpoll - Make a new poll.
    /seturl - set the URL for a poll - i.e. a Google Forms link.
    /settargetchat - set the "target chat" for a poll - only users present in this chat can vote in the poll.
    /settitle - set the name of a poll.
    /activate - enable voting on a poll.
    /deactivate - disable voting on a poll
/getchatid - Prints the Telegram chat_id for the current chat, for use with /settargetchat .
/listpolls - Lists all polls that belong to you.
/listtokens - Lists the tokens that have been issued for your poll."""

# For BotFather /setcommands
"""
help - Get help.
vote - Get a token to vote in an existing poll.
newpoll - Make a new poll.
seturl - set the URL for a poll - i.e. a Google Forms link.
settargetchat - set the "target chat" for a poll - only users present in this chat can vote in the poll.
settitle - set the name of a poll.
activate - enable voting on a poll.
deactivate - disable voting on a poll
getchatid - Prints the Telegram chat_id for the current chat, for use with /settargetchat .
listpolls - Lists all polls that belong to you.
listtokens - Lists the tokens that have been issued for your poll.
"""

import telegram


def cmd_help(bot: telegram.Bot, update: telegram.Update):
    cid = update.message.chat_id
    if update.message.chat.type != "private":
        bot.sendMessage(cid, text_private_chat_only)
        return

    bot.sendMessage(cid, text=text_help)


def cmd_start(bot: telegram.Bot, update: telegram.Update):
    cid = update.message.chat_id
    if update.message.chat.type != "private":
        bot.sendMessage(cid, text_private_chat_only)
        return

    bot.sendMessage(cid, text=text_start)
