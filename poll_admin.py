import telegram
from db import polls_db
from tinydb import Query
from text import text_private_chat_only
import tinydb

template = """Owner: {p[owner]}
Tag: {p[tag]}
Title: {p[title]}
Target Chat: {p[target_chat]}
URL: {p[url]}
Active: {p[active]}"""

def cmd_list_polls(bot: telegram.Bot, update: telegram.Update):
    uid = update.message.from_user.id
    cid = update.message.chat_id
    if update.message.chat.type != "private":
        bot.sendMessage(cid, text_private_chat_only)
        return

    q = Query()
    polls = polls_db.search(q.owner == uid)


    bot.sendMessage(cid, "You have %i polls:" % len(polls))
    for p in polls:
        msg = template.format(p=p)
        bot.sendMessage(cid, msg)