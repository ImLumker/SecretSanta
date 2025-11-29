from aiogram.types import Message
from functools import wraps

from bot.dispatcher import admins

def admin_only(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        user_id = message.from_user.id

        if user_id not in admins:
            return None
        return await func(message, *args, **kwargs)
    return wrapper
