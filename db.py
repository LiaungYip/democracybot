import random
import string

from tinydb import TinyDB, Query

polls_db = TinyDB("polls.json")
tokens_db = TinyDB("tokens.json")


def new_poll(owner: int):
    # Creates a new poll owned by the user_id "owner".
    #
    # The poll is identified by a unique 8-character code like "liokpqid".
    #
    # The poll starts out with "active": False.
    #
    # The user is expected to fill in the details using commands like
    #
    # /edit liokpqid url http://www.contoso.com
    #
    # then activate using
    #
    # /activate liokpqid
    q = Query()
    while True:
        # generate a unique tag, made of 8 characters a-z.
        tag = "".join([random.choice(string.ascii_lowercase) for i in range(8)])
        if not polls_db.contains(q.tag == tag):
            break

    polls_db.insert({
        "owner": owner,
        "target_chat": 0,
        "tag": tag,
        "title": "",
        "url": "",
        "active": False,
    })

    return tag


def polls_owned_by(owner: int):
    q = Query()
    results = polls_db.search(q.owner == owner)
    return results


def edit_poll(tag: str, field: str, value):
    assert field in ("title", "url", "target_chat", "active")
    q = Query()
    polls_db.update({field: value}, q.tag == tag)


def get_poll(tag: str):
    q = Query()
    return polls_db.get(q.tag == tag)

#
# poll_id = polls_db.insert(
#     {
#         "owner": 12345678,
#         "target_chat": 56789190,
#         "tag": "abcdefgh",
#         "title": "Cats or dogs?",
#         "url": "http://contoso.com/1",
#         "finished": False,
#         "active": True,
#     }
# )
#
# token_id = tokens_db.insert(
#     {
#         "poll_id": poll_id,
#         "tg_user_id": 98765432,
#         "token": "CantCombAHairyBall",
#     }
# )
#
# q = Query()
# results = tokens_db.search(q.poll_id == poll_id)
# tokens = [t['token'] for t in results]
# print(tokens)
#
# q = Query()
# results = polls_db.search(q.active == True)
# print([p['title'] for p in results])
