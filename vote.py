import random
import re
import string

import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, \
    Filters
from tinydb import Query

from db import polls_db, tokens_db
from text import text_vote_not_understood, text_no_such_vote, text_new_token, \
    text_existing_token, text_private_chat_only
from user_in_chat import user_is_in_chat

state_vote_1, state_vote_2 = range(2)


def cmd_vote(bot: telegram.Bot, update: telegram.Update):
    cid = update.message.chat_id
    uid = update.message.from_user.id
    polls = get_polls(uid, bot)

    if update.message.chat.type != "private":
        bot.sendMessage(cid, text_private_chat_only)
        return ConversationHandler.END

    if len(polls) == 0:
        bot.sendMessage(cid, "You aren't eligible to vote in any polls.")
    else:
        keyboard_choices = [p["tag"] + ": " + p["title"] for p in polls]
        # keyboard array is a list of lists
        # because each list represents a new row
        # and we want each button on a separate row
        keyboard_array = [[k, ] for k in keyboard_choices]
        keyboard = ReplyKeyboardMarkup(keyboard_array,
                                       one_time_keyboard=True)
        bot.sendMessage(cid,
                        "Click the button for the poll you would like to vote in.",
                        reply_markup=keyboard)
    return state_vote_1


def process_vote_response(bot: telegram.Bot, update: telegram.Update):
    # Message text comes from a reply keyboard.
    # The keyboard options look like: "abcdefgh: Title of Poll",
    # where "abcdefgh" is the poll tag.
    t = update.message.text
    uid = update.message.from_user.id

    # Check if user has typed something into the text reply, instead of
    # clicking a reply  keyboard button like they should have.
    if not re.match("^[a-z]{8}:", t):
        bot.sendMessage(update.message.chat_id, text_vote_not_understood,
                        reply_markup=ReplyKeyboardHide())
        return ConversationHandler.END

    # Check if the given poll tag 1) exists, 2) is active,
    # and 3) if the user is allowed to vote in that poll.
    poll_tag = t[0:8]

    q = Query()
    poll = polls_db.get(q.tag == poll_tag)

    if (poll is None) or (poll['active'] != True) or (
            not user_is_in_chat(uid, poll['target_chat'], bot)):
        bot.sendMessage(update.message.chat_id, text_no_such_vote,
                        reply_markup=ReplyKeyboardHide())
        return ConversationHandler.END

    # Check if user was already given a token for this poll.
    q2 = Query()
    existing_token = tokens_db.get(
        q2.user_id == uid and q2.poll_tag == poll_tag)

    if existing_token is None:
        # Give new token
        token = make_token(uid, poll_tag)
        msg = text_new_token.format(title=poll['title'], url=poll['url'],
                                    token=token)
        bot.sendMessage(update.message.chat_id, msg,
                        reply_markup=ReplyKeyboardHide())
        return ConversationHandler.END
    else:
        # Give existing token again
        token = existing_token['token']
        msg = text_existing_token.format(title=poll['title'], url=poll['url'],
                                         token=token)
        bot.sendMessage(update.message.chat_id, msg,
                        reply_markup=ReplyKeyboardHide())
        return ConversationHandler.END

    assert False  # Should never reach here


def vote_conversation_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("vote", cmd_vote)],
        states={
            state_vote_1: [
                MessageHandler([Filters.text], process_vote_response)],
        },
        fallbacks=[],
    )
    return conv_handler


def get_polls(user_id: int, bot: telegram.Bot):
    # Gets a list of polls that the given user_id is allowed to vote in.
    #    * The poll must be active.
    #    * The user must belong to the poll's target_chat. (This is determined
    #      by asking the Telegram API - "Does user 123 belong to chat -456?")
    all_polls = polls_db.all()

    # Convert to set to get unique values
    target_chats = set([p['target_chat'] for p in all_polls
                        if p['active'] == True])

    # Ask telegram API - is user 123 in chat -456?
    chats_user_is_in = [c for c in target_chats
                        if user_is_in_chat(user_id, c, bot)]

    valid_polls = [p for p in all_polls
                   if p['target_chat'] in chats_user_is_in
                   and p['active'] == True]

    return valid_polls


def make_token(user_id: int, poll_tag: str):
    q = Query()
    while True:
        # generate a unique token, made of 8 characters a-z.
        token = "".join(
            [random.choice(string.ascii_lowercase) for i in range(8)])
        if not tokens_db.contains(q.token == token):
            break

    tokens_db.insert({
        "user_id": user_id,
        "poll_tag": poll_tag,
        "token": token
    })

    return token
