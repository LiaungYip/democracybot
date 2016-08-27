import telegram

from db import new_poll
from text import text_new_poll, text_private_chat_only


def cmd_new_poll(bot: telegram.Bot, update: telegram.Update):
    cid = update.message.chat_id
    uid = update.message.from_user.id

    if update.message.chat.type != "private":
        bot.sendMessage(cid, text_private_chat_only)
        return

    poll_tag = new_poll(uid)
    # bot.sendMessage(cid, "Created a new poll: %s Registered to your user_id: %i" % (poll_tag, uid), parse_mode="Markdown")
    text = text_new_poll.format(p=poll_tag, u=uid)
    bot.sendMessage(cid, text, parse_mode="Markdown")
