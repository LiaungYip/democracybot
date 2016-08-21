import telegram

from db import new_poll

text_new_poll = """Created a new poll with tag:
`{p}`
Registered to your user id:
`{u}`
Edit it using the commands:
`/seturl {p} http://www.example.com/`
`/settitle {p} My Example Poll`
`/settargetchat {p} -12345678`

You can get the `targetchat` by adding the bot to your target chat, then calling `/getchatid` in that chat.

When you're done, activate it using:
`/activate {p}`
"""
text_private_chat_only = "This command only works in private chat with the bot."


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
