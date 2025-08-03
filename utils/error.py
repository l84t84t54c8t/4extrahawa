#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

import traceback
from functools import wraps

from AlinaMusic import app
from config import LOG_GROUP_ID
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line

    result.append(small_msg)

    return result


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            if isinstance(message, Message):
                await app.leave_chat(message.chat.id)
            elif isinstance(message, CallbackQuery):
                await app.leave_chat(message.message.chat.id)
            return
        except Exception as err:
            errors = traceback.format_exc()

            # Setup defaults
            user_mention = "❌"
            chat_info = "❌"
            command = "N/A"

            if isinstance(message, Message):
                user_mention = message.from_user.mention if message.from_user else "❌"
                chat_info = (
                    f"@{message.chat.username}"
                    if message.chat and message.chat.username
                    else f"`{message.chat.id}`" if message.chat else "❌"
                )
                command = message.text or message.caption or "❌"
            elif isinstance(message, CallbackQuery):
                user_mention = message.from_user.mention if message.from_user else "❌"
                chat = message.message.chat if message.message else None
                chat_info = (
                    f"@{chat.username}"
                    if chat and chat.username
                    else f"`{chat.id}`" if chat else "❌"
                )
                command = message.data or "❌"

            error_feedback = split_limits(
                f"**ERROR** | {user_mention} | {chat_info}\n"
                f"```command\n{command}```\n\n"
                f"```python\n{''.join(errors)}```\n"
            )

            for x in error_feedback:
                await app.send_message(LOG_GROUP_ID, x)

            raise err

    return capture
