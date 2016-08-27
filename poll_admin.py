import telegram
from tinydb import Query

from db import polls_db
from db import tokens_db
from edit_poll import generic_checks
from text import text_private_chat_only

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


def cmd_list_tokens(bot: telegram.Bot, update: telegram.Update):
    cid = update.message.chat_id

    if generic_checks(bot, update, "listtokens", "", 1):
        # Extract value
        text = update.message.text
        cmd, tag = text.split(" ", 1)

        q = Query()
        tokens = tokens_db.search(q.poll_tag == tag)

        msg = "There have been %i tokens generated for your poll:\n" % len(
            tokens)
        msg = msg + "\n".join(
            ["%i: %s" % (n + 1, t['token']) for n, t in enumerate(tokens)])

        bot.sendMessage(cid, msg)
