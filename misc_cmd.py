# def get_user_id(bot, update):
#     cid = update.message.chat_id
#     uid = update.message.from_user.id
#     text = "Your user ID is:\n`%s`" % uid
#     bot.sendMessage(cid, text=text, parse_mode="Markdown")

def cmd_get_chat_id(bot, update):
    # /get_chat_id prints the Telegram chat_id to the chat.
    cid = update.message.chat_id
    text = "The Chat ID for this chat is:\n`%s`" % cid
    bot.sendMessage(cid, text=text, parse_mode="Markdown")
