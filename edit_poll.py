import re

import telegram

from db import get_poll, edit_poll
from new_poll import text_private_chat_only

text_not_enough_parts = """I don't think you typed that right.
Try something like:
`/{c} etaoinsh {e}`
Where `etaoish` is your "poll tag"."""

text_malformed_tag = """There's no such tag `{t}`.
Tags should be 8 lowercase letters, like `etaoinsh`.
Check your spelling of `{t}` and try again.
Or maybe try `/newpoll` to make a new poll."""

text_no_such_tag_or_not_owner = """Either there's no poll called `{t}`, or you don't own `{t}`.
Check your spelling of `{t}` and try again.
Or maybe try `/newpoll` to make a new poll."""

text_edit_successful = """
Changes applied!
Your poll looks like this now:
Owner: {p[owner]}
Tag: {p[tag]}
Title: {p[title]}
Target Chat: {p[target_chat]}
URL: {p[url]}
Active: {p[active]}
"""

text_activate_suggestion = """Your setup looks complete!
Use `/activate {t}` to activate your poll.
Once active, people will be able to ask for vote tokens using `/vote`."""

text_not_ready_to_activate = """That poll doesn't look ready yet.
Have you filled out the title, target chat, and url?
"""

text_activation_complete = """Your poll is active!

People can ask for vote tokens by:

- Opening a private message with the bot
- Sending the /vote command, which will give them a list of polls they can vote in.

They will only see your poll if they belong to the target chat."""

text_deactivated = """Your poll is de-activated.

People will no longer be able to see it with the /vote command."""


# ------------------------------------------------------------------------------
# Generic checks for all commands used by poll owners
# ------------------------------------------------------------------------------

def generic_checks(bot: telegram.Bot, update: telegram.Update,
                   cmd_name: str, example: str, num_arguments_required: int):
    cid = update.message.chat_id
    uid = update.message.from_user.id
    text = update.message.text

    # return True if OK
    # return False if a test fails

    # Don't allow this command in an actual chat room
    if update.message.chat.type != "private":
        bot.sendMessage(cid, text_private_chat_only)
        return False

    # Detect if the user typed enough arguments
    parts = text.split(" ", num_arguments_required)
    if len(parts) < num_arguments_required + 1:
        msg = text_not_enough_parts.format(c=cmd_name, e=example)
        bot.sendMessage(cid, msg, parse_mode="Markdown")
        return False

    # Detect if the user typed a valid tag like `etaoinsh`
    tag = parts[1]
    if not re.match("^[a-z]{8}$", tag):
        msg = text_malformed_tag.format(t=tag)
        bot.sendMessage(cid, msg, parse_mode="Markdown")
        return False

    # Detect if the user actually owns the specified tag. (Don't let users
    # edit other users' polls)
    p = get_poll(tag)
    if p is None or p["owner"] != uid:
        msg = text_no_such_tag_or_not_owner.format(t=tag)
        bot.sendMessage(cid, msg, parse_mode="Markdown")
        return False

    # All tests pass
    return True


# ------------------------------------------------------------------------------
# settitle, seturl, settargetchat
# ------------------------------------------------------------------------------

def cmd_set_generic(bot: telegram.Bot, update: telegram.Update, field_name: str,
                    cmd_name: str, example: str):
    if generic_checks(bot, update, cmd_name, example, 2):
        # Extract value
        text = update.message.text
        cmd, tag, value = text.split(" ", 2)

        # Apply edit and
        edit_poll(tag, field_name, value)

        # send "success" feedback message
        new_p = get_poll(tag)
        msg = text_edit_successful.format(p=new_p)
        cid = update.message.chat_id
        bot.sendMessage(cid, msg)

        # Check if complete, and suggest to activate
        if check_if_complete(tag):
            msg2 = text_activate_suggestion.format(t=tag)
            bot.sendMessage(cid, msg2, parse_mode="Markdown")
    else:
        # A generic check failed.
        pass

    return


def cmd_set_title(bot: telegram.Bot, update: telegram.Update):
    cmd_set_generic(bot, update, "title", "settitle", "Example Poll Title")


def cmd_set_url(bot: telegram.Bot, update: telegram.Update):
    cmd_set_generic(bot, update, "url", "seturl",
                    "http://www.example.com/mypoll")


def cmd_set_target_chat(bot: telegram.Bot, update: telegram.Update):
    cmd_set_generic(bot, update, "target_chat", "settargetchat", "-12345678")


# ------------------------------------------------------------------------------
# Activate / Deactivate
# ------------------------------------------------------------------------------

def cmd_activate_deactivate(bot: telegram.Bot, update: telegram.Update,
                            active: bool):
    cmd = "activate" if active else "deactivate"
    if generic_checks(bot, update, cmd, "", 1):
        # Extract value
        text = update.message.text
        cmd, tag = text.split(" ", 1)

        # Apply edit
        edit_poll(tag, "active", active)

        # send "success" feedback message
        new_p = get_poll(tag)
        msg = text_edit_successful.format(p=new_p)
        cid = update.message.chat_id
        bot.sendMessage(cid, msg)

        if active:
            bot.sendMessage(cid, text_activation_complete,
                            parse_mode="Markdown")
        else:
            bot.sendMessage(cid, text_deactivated)

    else:
        # A generic check failed.
        pass


def cmd_activate(bot: telegram.Bot, update: telegram.Update):
    cmd_activate_deactivate(bot, update, True)


def cmd_deactivate(bot: telegram.Bot, update: telegram.Update):
    cmd_activate_deactivate(bot, update, False)


# ------------------------------------------------------------------------------
# Check if poll is complete, and suggest to activate
# ------------------------------------------------------------------------------

def check_if_complete(tag: str):
    p = get_poll(tag)
    if p['title'] != "" and p['url'] != "" and p['target_chat'] != 0 and p[
        'active'] == False:
        return True
    else:
        return False
