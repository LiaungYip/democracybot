text_vote_not_understood = """I didn't understand that.
Try /vote again, and click one of the buttons that appears at the bottom of your screen."""

text_no_such_vote = """There's no such poll to vote in (or you can't vote in it.)
Try /vote again, and click one of the buttons that appears at the bottom of your screen."""

text_new_token = """Great!

I'm issuing you a token to vote in the poll {title}.
Go to this link to vote: {url}
The voting form should have a space for your "vote token".

Your vote token is: {token}

Your vote token is unique to you, and unique to this poll.
Your vote token is anonymous - nobody knows who you are, except this Telegram bot (and we promise not to tell!)
When the vote results are published, you can use your token to check if your vote was recorded accurately.
"""

text_existing_token = """Great!

You already have a token to vote in the poll: {title}.
Go to this link to vote: {url}
The voting form should have a space for your "vote token".

Your vote token was: {token}

* Your vote token is unique to you, and unique to this poll.
* Your vote token is anonymous - nobody knows who you are, except this Telegram bot (and we promise not to tell!)
* When the vote results are published, you can use your token to check if your vote was recorded accurately.
"""

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
