import logging
from functools import wraps
from traceback import format_exc

from AlinaMusic import app
from AlinaMusic.misc import SUDOERS
from pyrogram.errors import ChatWriteForbidden
from pyrogram.types import Message

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def member_permissions(chat_id: int, user_id: int) -> list[str]:
    """Fetches the permissions of a member in a chat."""
    member = (await app.get_chat_member(chat_id, user_id)).privileges
    return (
        [
            perm
            for perm, has_perm in {
                "can_post_messages": member.can_post_messages,
                "can_edit_messages": member.can_edit_messages,
                "can_delete_messages": member.can_delete_messages,
                "can_restrict_members": member.can_restrict_members,
                "can_promote_members": member.can_promote_members,
                "can_change_info": member.can_change_info,
                "can_invite_users": member.can_invite_users,
                "can_pin_messages": member.can_pin_messages,
                "can_manage_video_chats": member.can_manage_video_chats,
            }.items()
            if has_perm
        ]
        if member
        else []
    )


async def bot_permissions(chat_id: int):
    perms = []
    return await member_permissions(chat_id, app.id)


async def authorised(func, subFunc2, client, message, *args, **kwargs):
    chatID = message.chat.id
    try:
        await func(client, message, *args, **kwargs)
    except ChatWriteForbidden:
        await client.leave_chat(chatID)
    except Exception as e:
        logging.exception(e)  # Logs full error traceback
        try:
            await message.reply_text(str(getattr(e, "MESSAGE", e)))
        except Exception:
            await message.reply_text(str(e))  # Fallback message
    return subFunc2


async def unauthorised(
    message: Message, permission, subFunc2, bot_lacking_permission=False
):
    chatID = message.chat.id

    if bot_lacking_permission:
        text = (
            f"**🤖 | من ئەدمین نیم لێرە!**"
            f"**\n⛔️ | پێویستم بە ڕۆڵی __{permission}__ هەیە لە گرووپەکە.**"
        )
    else:
        text = (
            "**👮🏻 | ببورە، تۆ ڕۆڵت نییە**"
            + f"\n**👮🏻 | پێویستە ڕۆڵی** __{permission}__ هەبێت !**"
        )

    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await client.leave_chat(chatID)

    return subFunc2


def adminsOnly(permission):
    def subFunc(func):
        @wraps(func)
        async def subFunc2(client, message: Message, *args, **kwargs):
            chatID = message.chat.id

            # Check if the bot has the required permission
            bot_perms = await bot_permissions(chatID)
            if permission not in bot_perms:
                return await unauthorised(
                    message, permission, subFunc2, bot_lacking_permission=True
                )

            if not message.from_user:
                # For anonymous admins
                if message.sender_chat and message.sender_chat.id == message.chat.id:
                    return await authorised(
                        func,
                        subFunc2,
                        client,
                        message,
                        *args,
                        **kwargs,
                    )
                return await unauthorised(message, permission, subFunc2)

            # For admins and sudo users
            userID = message.from_user.id
            permissions = await member_permissions(chatID, userID)
            if userID not in SUDOERS and permission not in permissions:
                return await unauthorised(message, permission, subFunc2)
            return await authorised(func, subFunc2, client, message, *args, **kwargs)

        return subFunc2

    return subFunc
