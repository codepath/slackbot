from functools import wraps


def channel_response_deprecated(fn):
    @wraps(fn)
    def wrapper(res, *args, **kwargs):
        if res.message.is_direct_message:
            return fn(res, *args, **kwargs)

        res.send(
            "Hi there! In an effort make this channel more useful "
            "and less spammy, I only respond in DMs now. Please DM me "
            "your query instead and I'd be happy to help",
        )

    return wrapper
