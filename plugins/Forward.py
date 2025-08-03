from AlinaMusic import app
from AlinaMusic.core.mongo import mongodb
from AlinaMusic.misc import SUDOERS
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChannelPrivate,
    ChatAdminRequired,
    PeerIdInvalid,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


antiforwarddb = mongodb.antiforward  # <-- new collection


async def enable_forward_lock(chat_id: int):
    await antiforwarddb.update_one(
        {"chat_id": chat_id}, {"$set": {"locked": True}}, upsert=True
    )


async def disable_forward_lock(chat_id: int):
    await antiforwarddb.update_one(
        {"chat_id": chat_id}, {"$set": {"locked": False}}, upsert=True
    )


async def is_forward_locked(chat_id: int) -> bool:
    data = await antiforwarddb.find_one({"chat_id": chat_id})
    if data is None:
        return True
    return data.get("locked", True)



@app.on_message(
    filters.command(["/antiforward", "فۆروارد", "/forward", "ناردنی فۆروارد"], "")
    & filters.group,
    group=300,
)
async def forward_lock_menu(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        member = await client.get_chat_member(chat_id, user_id)
        if not (
            member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
            or user_id in SUDOERS
        ):
            return await message.reply("🚫 تەنها ئەدمینەکان دەتوانن فەرمان بەکاربهێنن.")
    except Exception:
        return await message.reply("❌ ناتوانرێت بزانرێت ئەدمینە یان نا.")

    locked = await is_forward_locked(chat_id)
    text = f"**🔒 سیستەمی فۆروارد:**\n\nدۆخی فۆروارد: {'❌ داخراوە' if locked else '✅ کراوەتەوە'}"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❌ داخستنی فۆروارد", callback_data=f"forwardlock:on:{chat_id}"
                ),
                InlineKeyboardButton(
                    "✅ کردنەوەی فۆروارد", callback_data=f"forwardlock:off:{chat_id}"
                ),
            ]
        ]
    )

    await message.reply(text, reply_markup=buttons)


@app.on_callback_query(filters.regex(r"^forwardlock:(on|off):(-?\d+)$"))
async def handle_forward_lock_callback(client, cb):
    action, chat_id = cb.data.split(":")[1:]
    chat_id = int(chat_id)
    user_id = cb.from_user.id

    try:
        member = await client.get_chat_member(chat_id, user_id)
        if not (
            member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
            or user_id in SUDOERS
        ):
            return await cb.answer(
                "🚫 تەنها ئەدمینەکان دەتوانن فەرمان بەکاربهێنن.", show_alert=True
            )
    except Exception:
        return await cb.answer("❌ ناتوانرێت ئەنجام بدرێ.", show_alert=True)

    is_locked = await is_forward_locked(chat_id)

    if action == "on":
        if is_locked:
            return await cb.answer("⚠️ پێشتر داخراوە.", show_alert=True)
        await enable_forward_lock(chat_id)
        await cb.message.edit_text("**❌ ناردنی فۆروارد داخرا.**")
    else:
        if not is_locked:
            return await cb.answer("⚠️ پێشتر کراوەتەوە.", show_alert=True)
        await disable_forward_lock(chat_id)
        await cb.message.edit_text("**✅ ناردنی فۆروارد کرایەوە.**")

    await cb.answer()


@app.on_message(filters.group & filters.forwarded, group=16)
async def auto_delete_forwarded_messages(client, message):
    chat_id = message.chat.id

    if message.sender_chat:
        return

    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        return

    if not await is_forward_locked(chat_id):
        return

    try:
        chat_member = await client.get_chat_member(chat_id, user_id)
    except UserNotParticipant:
        return
    except (PeerIdInvalid, ChannelPrivate, ChatAdminRequired):
        return
    except Exception:
        return

    if chat_member.status != ChatMemberStatus.MEMBER:
        return

    try:
        await message.delete()
    except Exception:
        pass
