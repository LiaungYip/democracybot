def cmd_get_chat_id(bot, update):
    # /get_chat_id prints the Telegram chat_id to the chat.
    cid = update.message.chat_id
    chat_type = update.message.chat.type
    if chat_type == "private":
        text = "/getchatid is supposed to be used in a chat group, not in private messages with the bot."
    else:
        text = "The Chat ID for this chat is:\n`%s`" % cid

    bot.sendMessage(cid, text=text, parse_mode="Markdown")
