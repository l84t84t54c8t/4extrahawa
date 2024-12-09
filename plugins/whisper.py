from AlinaMusic import app
from pyrogram import enums, filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InlineQueryResultPhoto,
                            InputTextMessageContent)

######################
LOG = -1002105278394
######################


@app.on_message(filters.command("wstart") & filters.private)
async def startmsg(app, message):
    text = """**
👋 سڵاو {}

❓ چۆن چرپە بەکاربێنم :

`@HawalmusicBot سلاو @Hawaallll`
`@HawalmusicBot سلاو @all`

**""".format(
        message.from_user.mention
    )
    key = InlineKeyboardMarkup(
        [[InlineKeyboardButton("تاقیکردنەوە", switch_inline_query="سلاو @Hawaallll")]]
    )
    await message.reply(text, reply_markup=key, quote=True)


@app.on_inline_query(filters.regex("@"))
async def whisper(app, iquery):
    user = iquery.query.split("@")[1]
    if " " in user:
        return
    user_id = iquery.from_user.id
    query = iquery.query.split("@")[0]
    if user == "all":
        text = "**🎊 ئەم چرپەیە بۆ هەمووانە**"
        username = "all"
    else:
        get = await app.get_chat(user)
        user = get.id
        username = get.first_name
        text = (
            f"**🔒 چرپەنامەیەك بۆ  ( {username} )\nتەنیا ئەو دەتوانێت نامەکە بکاتەوە**"
        )
    send = await app.send_message(LOG, query)
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "پیشاندانی نامە 🔐",
                    callback_data=f"{send.id}geting{user}from{user_id}",
                )
            ]
        ]
    )
    await iquery.answer(
        results=[
            InlineQueryResultArticle(
                title=f"📪 چرپەنامەیەكت نارد بۆ {username}",
                url="http://t.me/Haawall",
                input_message_content=InputTextMessageContent(
                    message_text=text, parse_mode=enums.ParseMode.MARKDOWN
                ),
                reply_markup=reply_markup,
            )
        ],
        cache_time=1,
    )


@app.on_inline_query()
async def whisper(app, query):
    text = """**
❓ چۆن چرپە بەکاربێنم :

`@HawalmusicBot سلاو @Hawaallll`
`@HawalmusicBot سلاو @all`

**"""
    await query.answer(
        results=[
            InlineQueryResultPhoto(
                title="🔒 چرپەنامە لەگەڵ + یوزەر",
                photo_url="https://t.me/Hawaallll",
                description="@HawalmusicBot hi @Hawaallll",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔗", url="t.me/Haawall")]]
                ),
                input_message_content=InputTextMessageContent(text),
            ),
        ],
        cache_time=1,
    )


@app.on_callback_query(filters.regex("geting"))
async def get_whisper(app, query):
    sp = query.data.split("geting")[1]
    user = sp.split("from")[0]
    from_user = int(sp.split("from")[1])
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("پیشاندانی نامە 🔐", callback_data=query.data)],
            [InlineKeyboardButton("🗑️", callback_data=f"DELETE{from_user}")],
        ]
    )
    if user == "all":
        msg = await app.get_messages(LOG, int(query.data.split("geting")[0]))
        await query.answer(msg.text, show_alert=True)
        try:
            await query.edit_message_reply_markup(reply_markup)
        except BaseException:
            pass
        try:
            alert0 = f"📭 {query.from_user.mention} کرایەوە @all چرپەنامەی"
            await app.send_message(from_user, alert0)
        except BaseException:
            pass
        return

    else:
        if str(query.from_user.id) == user:
            msg = await app.get_messages(LOG, int(query.data.split("geting")[0]))
            await query.answer(msg.text, show_alert=True)
            try:
                await query.edit_message_reply_markup(reply_markup)
            except BaseException:
                pass
            return

        if query.from_user.id == from_user:
            msg = await app.get_messages(LOG, int(query.data.split("geting")[0]))
            await query.answer(msg.text, show_alert=True)
            return

        else:
            get = await app.get_chat(int(user))
            touser = get.first_name
            alert = f"**کەسێك هەوڵیدا چرپەی تۆ بکاتەوە {touser}:\n\n**"
            alert += f"👤 ناو : {query.from_user.mention}\n"
            alert += f"🆔 ئایدی : {query.from_user.id}\n"
            if query.from_user.username:
                alert += f"🔍 یوزەر : @{query.from_user.username}\n"
            alert += "\n\n📭"
            await query.answer("🔒 ئەم چرپەیە بۆتۆ نییە بەڕێزم", show_alert=True)
            try:
                await app.send_message(from_user, alert)
            except BaseException:
                pass
            return


@app.on_callback_query(filters.regex("DELETE"))
async def del_whisper(app, query):
    user = int(query.data.split("DELETE")[1])
    if not query.from_user.id == user:
        return await query.answer("❓ تەنیا ئەو کەسە دەتوانێت کە ناردوویەتی")

    else:
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("خاوەنی بۆت 🔗", url="https://t.me/Hawaallll")]]
        )
        await query.edit_message_text(
            f"**🗑️ چرپەنامە سڕدرایەوە لەلایەن : ( {query.from_user.mention} ) .**",
            reply_markup=reply_markup,
        )


__MODULE__ = "Wʜɪsᴘᴇʀ"
__HELP__ = """
**Wʜɪsᴘᴇʀ**

- Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴜsᴇᴅ ᴛᴏ sᴇɴᴅ ᴀ sᴇᴄʀᴇᴛ ᴍᴇssᴀɢᴇ ɪɴ ɢʀᴏᴜᴘs ᴛʜᴀᴛ ᴏɴʟʏ ᴀ ᴅᴇsɪɢɴᴀᴛᴇᴅ ᴘᴇʀsᴏɴ ᴄᴀɴ ᴏᴘᴇɴ

**ᴜsᴀɢᴇ :**
- ᴜsᴇʀɴᴀᴍᴇ ʙᴏᴛ + ᴍᴇssᴀɢᴇ + ᴜsᴇʀɴᴀᴍᴇ ᴘᴇʀsᴏɴ
- ᴜsᴇʀɴᴀᴍᴇ ʙᴏᴛ + ᴍᴇssᴀɢᴇ + ᴀʟʟ
- Iғ ʏᴏᴜ ᴜsᴇ ᴛʜᴇ ᴡᴏʀᴅ « Aʟʟ » ɪɴsᴛᴇᴀᴅ ᴏғ ᴛʜᴇ ᴜsᴇʀɴᴀᴍᴇ, ᴛʜᴇ ᴍᴇssᴀɢᴇ ɪs ғᴏʀ ᴀʟʟ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs

**ᴇxᴀᴍᴘʟᴇ : **
- @HawalmusicBot Hɪ Bʀᴏ @Hawaallll
- @HawalmusicBot Hɪ Gᴜʏs all
"""
