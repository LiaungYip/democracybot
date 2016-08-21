import logging

import telegram

logger = logging.getLogger(__name__)

err_chat_not_found = """in user_is_in_chat():
Called with uid = %s and cid = %s
Telegram returned 'Chat not found'.
Either:
- The bot isn't in that chat, or;
- That chat doesn't exist at all.
"""
err_user_not_found = """in user_is_in_chat():
Called with uid = %s and cid = %s
Telegram returned 'User not found'.
Either:
- That user isn't in that chat, or;
- That user doesn't exist at all.
"""


def user_is_in_chat(uid: int, cid: int, bot: telegram.Bot):
    # Returns True if the specified user_id is in the specified chat_id.
    #
    # Returns False if:
    # * the bot isn't in the chat (so it can't see the members), or;
    # * the chat doesn't exist, or;
    # * the user isn't in the chat, or;
    # * the user doesn't exist.

    try:
        user = bot.get_chat_member(chat_id=cid, user_id=uid)
    except telegram.error.BadRequest as err:
        if "chat not found" in err.message.lower():
            logger.info(err_chat_not_found % (uid, cid))
            return False
        elif "user not found" in err.message.lower():
            logger.info(err_user_not_found % (uid, cid))
            return False
        else:
            logger.exception("Unhandled exception")
            raise
    logger.info("User %s is in chat %s" % (uid, cid))
    return True
