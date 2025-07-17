from datetime import datetime

from AlinaMusic import app
from AlinaMusic.core.mongo import mongodb
from AlinaMusic.misc import SUDOERS
from config import LOG_GROUP_ID
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


# Constants
GLOBAL_ID = "global"

# MongoDB collections
join_config_collection = mongodb.join_config
join_log_collection = mongodb.join_logs


async def get_join_config():
    doc = await join_config_collection.find_one({"_id": GLOBAL_ID})
    if not doc:
        return [], True
    return doc.get("forced_channels", []), doc.get("join_required", True)


async def update_join_config(forced_channels=None, join_required=None):
    update_data = {}
    if forced_channels is not None:
        update_data["forced_channels"] = forced_channels
    if join_required is not None:
        update_data["join_required"] = join_required

    if update_data:
        await join_config_collection.update_one(
            {"_id": GLOBAL_ID}, {"$set": update_data}, upsert=True
        )


async def log_join_check(user_id: int, passed: bool, channels: list):
    await join_log_collection.insert_one(
        {
            "user_id": user_id,
            "passed": passed,
            "channels_checked": channels,
            "timestamp": datetime.utcnow(),
        }
    )


async def send_log_to_channel(client, user_id: int, passed: bool, channels: list):
    try:
        user = await client.get_users(user_id)
        mention = f"[{user.first_name}](tg://user?id={user.id})"
    except Exception:
        mention = f"`{user_id}`"

    status = "**✅ جۆینی کرد**" if passed else "**❌ جۆینی نەکرد**"
    chan_text = ", ".join(channels) if channels else "No Channels"
    time_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    text = (
        f"{status}\n"
        f"**👤 بەکارهێنەر:** {mention} (`{user_id}`)\n"
        f"**📎 کەناڵەکان:** `{chan_text}`\n"
        f"**⏱ کات:** `{time_str}`"
    )

    try:
        await client.send_message(LOG_GROUP_ID, text)
    except Exception as e:
        print(f"❌ Failed to send log: {e}")


# ----------- SUDOERS COMMAND HANDLER -----------


@app.on_message(filters.text & filters.private & SUDOERS, group=4377)
async def handle_sudo_commands(client: Client, message: Message):
    user_id = message.from_user.id
    text = message.text.strip().lower()
    forced_channels, join_required = await get_join_config()

    if text in ["زیادکردنی جۆین", "زیادکردنی کەناڵ", "add join"]:
        reply = await message.chat.ask(
            "**• ئێستا یوزەر یان لینکی کەناڵ بنێرە\n• دەتوانی زیاتر لە یەک کەناڵ زیادبکەیت\n• تەنیا یوزەر/لینک با بۆشایان هەبێت**\n- `@MGIMT @EHS4SS`",
            filters=filters.text & filters.user(user_id),
            reply_to_message_id=message.id,
        )
        raw_input = reply.text.strip()
        input_channels = []
        for raw in raw_input.split():
            clean = raw.strip()
            if clean.startswith("https://t.me/"):
                slug = clean.replace("https://t.me/", "").strip("/")
                input_channels.append(slug)
            elif clean.startswith("t.me/"):
                slug = clean.replace("t.me/", "").strip("/")
                input_channels.append(slug)
            else:
                input_channels.append(clean.lstrip("@"))

        added, skipped, failed, not_admin = 0, 0, [], []
        bot_id = (await client.get_me()).id

        for channel in input_channels:
            try:
                chat = await client.get_chat(channel)

                # Check channel type
                if chat.type != ChatType.CHANNEL:
                    failed.append(channel)
                    continue

                # Check if bot is ADMINISTRATOR
                member = await client.get_chat_member(chat.id, bot_id)
                if member.status != ChatMemberStatus.ADMINISTRATOR:
                    not_admin.append(channel)
                    continue

                if channel not in forced_channels:
                    forced_channels.append(channel)
                    added += 1
                else:
                    skipped += 1
            except Exception:
                failed.append(channel)

        await update_join_config(forced_channels=forced_channels)

        msg = f"**✅ {added} کەناڵ زیادکرا.\n**" if added else ""
        msg += f"**⚠️ {skipped} پێشتر زیادکراوە\n**" if skipped else ""
        msg += f"**❌ هەڵەیەک ڕوویدا لە:** {' | '.join(failed)}\n" if failed else ""
        msg += (
            f"**🚫 بۆت ئەدمین نییە لە:** {' | '.join(not_admin)}" if not_admin else ""
        )
        await message.reply(msg or "**❌ هیچ کەناڵێک زیاد نەکرا.**")

    elif text in ["لیستی جۆین", "لیستی کەناڵەکان", "show join list"]:
        if not forced_channels:
            return await message.reply("**❌ لیستی کەناڵی جۆین بەتاڵە.**")

        buttons = [
            [
                InlineKeyboardButton(
                    f"❌ سڕینەوە {c}", callback_data=f"remove_channel:{c}"
                )
            ]
            for c in forced_channels
        ]
        buttons.append(
            [InlineKeyboardButton("📥 من جۆینم کردە", callback_data="check_join")]
        )
        await message.reply(
            "**📋 لیستی کەناڵەکان:**\n", reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif text in ["سڕینەوەی جۆین", "سڕینەوەی کەناڵ", "remove join"]:
        reply = await message.chat.ask(
            "**• یوزەری کەناڵ بنێرە\n• دەتوانی کەناڵەکان پێکەوە بسڕیتەوە**\n- `@MGIMT @EHS4SS`",
            filters=filters.text & filters.user(user_id),
            reply_to_message_id=message.id,
        )
        raw_input = reply.text.strip()
        channels = [c.lstrip("@") for c in raw_input.split() if c.strip()]
        removed, not_found = 0, 0

        for channel in channels:
            if channel in forced_channels:
                forced_channels.remove(channel)
                removed += 1
            else:
                not_found += 1

        await update_join_config(forced_channels=forced_channels)
        msg = f"**🗑️ {removed} کەناڵ سڕدرایەوە.\n" if removed else ""
        msg += f"❌ {not_found} نەدۆزرایەوە." if not_found else ""
        await message.reply(msg or "**❌ هیچ کەناڵێک نە سڕدرایەوە.**")

    elif text in ["چالاککردنی جۆینی ناچاری", "enable join"]:
        await update_join_config(join_required=True)
        await message.reply("**✅ بە سەرکەوتوویی جۆینی ناچاری چالاککرا.**")

    elif text in ["ناچالاککردنی جۆینی ناچاری", "disable join"]:
        await update_join_config(join_required=False)
        await message.reply("**🚫 بە سەرکەوتوویی جۆینی ناچاری لەکارخرا.**")


# ----------- CALLBACK HANDLERS -----------


@app.on_callback_query(filters.regex("remove_channel:"))
async def remove_channel_button(client: Client, callback: CallbackQuery):
    if callback.from_user.id not in SUDOERS:
        return await callback.answer(
            "⛔ ئەم فەرمانە تەنها بۆ گەشەپێدەرەکانە.", show_alert=True
        )

    channel = callback.data.split("remove_channel:")[1]
    forced_channels, _ = await get_join_config()

    if channel in forced_channels:
        forced_channels.remove(channel)
        await update_join_config(forced_channels=forced_channels)
        await callback.answer(f"🗑️ {channel} سڕدرایەوە.", show_alert=True)
        await callback.message.delete()
    else:
        await callback.answer("❌ ئەم کەناڵە زیادنەکراوە.", show_alert=True)


@app.on_callback_query(filters.regex("check_join"))
async def check_join_button(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    forced_channels, join_required = await get_join_config()
    await callback.answer("🔍 پشکنین دەکەم ...")

    if not join_required or not forced_channels:
        await log_join_check(user_id, True, [])
        await send_log_to_channel(client, user_id, True, [])
        return await callback.message.reply("**✅ ئێستا دەتوانی بۆت بەکاربهێنێت.**")

    not_joined = []
    for c in forced_channels:
        try:
            await client.get_chat_member(c, user_id)
        except Exception:
            not_joined.append(c)

    if not not_joined:
        await log_join_check(user_id, True, forced_channels)
        await send_log_to_channel(client, user_id, True, forced_channels)
        await callback.message.reply("**• تۆ جۆینت کردووە.**")
    else:
        await log_join_check(user_id, False, forced_channels)
        await send_log_to_channel(client, user_id, False, forced_channels)
        buttons = [
            [InlineKeyboardButton("🔁 دووبارە پشکنین بکە", callback_data="check_join")]
        ]
        await callback.message.reply(
            "**❌ هێشتا جۆینی هەموو کەناڵەکانت نەکردووە!**",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


# ----------- ENFORCE JOIN ON ALL USER MESSAGES -----------


@app.on_message(filters.incoming & filters.private, group=-3)
async def enforce_join(client: Client, message: Message):
    user_id = message.from_user.id
    forced_channels, join_required = await get_join_config()
    if not join_required or not forced_channels or user_id in SUDOERS:
        return

    not_joined = []
    for c in forced_channels:
        try:
            await client.get_chat_member(c, user_id)
        except Exception:
            not_joined.append(c)

    if not_joined:
        buttons = []
        for c in not_joined:
            url = (
                f"https://t.me/{c}"
                if not c.startswith(("t.me/", "https://"))
                else (c if c.startswith("https://t.me/") else f"https://{c}")
            )
            buttons.append(
                [InlineKeyboardButton("📥 ئێرە دابگرە بۆ کەناڵەکان", url=url)]
            )
        buttons.append(
            [
                InlineKeyboardButton(
                    "✅ من جۆینی هەموویانم کرد", callback_data="check_join"
                )
            ]
        )

        await message.reply(
            "**• پێویستە جۆینی هەموو کەناڵەکان بکەیت\n• تاوەکو بتوانیت بۆت بەکاربھێنیت:**",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        await message.stop_propagation()


# ----------- SHOW JOIN LOGS FOR SUDOERS -----------


@app.on_message(filters.command("joinlogs") & filters.private & SUDOERS, group=3478)
async def show_join_logs(client, message):
    logs_cursor = join_log_collection.find().sort("timestamp", -1).limit(20)
    logs = await logs_cursor.to_list(length=20)

    if not logs:
        return await message.reply("❌ هیچ ڕاپۆرتێک نەدۆزرایەوە.")

    text = "📋 **ئامارەکانی جۆینی ناچاری:**\n\n"
    for log in logs:
        status = "**✅ جۆینی کردووە**" if log.get("passed") else "**❌ جۆینی نەکردووە**"
        user_id = log.get("user_id", "Unknown")
        chan_list = ", ".join(log.get("channels_checked", [])) or "None"
        time = log.get("timestamp")
        if isinstance(time, datetime):
            time_str = time.strftime("%Y-%m-%d %H:%M UTC")
        else:
            time_str = str(time)

        text += (
            f"{status} | 👤 [{user_id}](tg://user?id={user_id}) | ⏱ {time_str}\n"
            f"**📎 کەناڵەکان:** `{chan_list}`\n\n"
        )

    if len(text) > 4000:
        text = text[:4000] + "\n\n(…too long, truncated)"

    await message.reply(text)
