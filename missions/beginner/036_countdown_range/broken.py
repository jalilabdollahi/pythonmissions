# Mission 036 - Release Countdown Blank
# Build the pre-release countdown the deploy bot posts to chat.


def countdown_messages(seconds):
    messages = []
    for remaining in range(seconds, 0):
        messages.append(f"T-{remaining}")
    messages.append("GO")
    return messages


def announce(seconds, post):
    messages = countdown_messages(seconds)
    for message in messages:
        post(message)
    return len(messages)
