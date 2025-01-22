import random

import requests
from AlinaMusic import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

SUPPORT_CHAT = "Haawall"


@app.on_message(
    filters.command(
        ["wish", "حەز", "هیوا", "خۆزگە"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
)
async def wish(_, m):
    if not m.text or len(m.command) < 2:
        await m.reply("**لەگەڵ فەرمانەکە خۆزگە یان حەزەکانت بنووسە 🥺🫶🏻**")
        return

    api = requests.get("https://nekos.best/api/v2/happy").json()
    url = api["results"][0]["url"]
    text = m.text.split(None, 1)[1]
    wish_count = random.randint(1, 100)

    # Check if the message is from a group or a channel
    if m.from_user:
        user_name = m.from_user.first_name
    elif m.sender_chat:
        user_name = m.sender_chat.title  # Use channel title if from a channel
    else:
        user_name = "ناو نەدۆزرایەوە"  # Fallback if no user or channel

    wish = f"**🍓 سڵاو {user_name}!**\n"
    wish += f"**🍓 حەزی تۆ: {text} **\n\n"
    wish += f"**🍓 ڕێژەی ڕوودانی: {wish_count}% **"

    await app.send_animation(
        chat_id=m.chat.id,
        animation=url,
        caption=wish,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "نوێکارییەکانی بۆت 🍻", url=f"https://t.me/{SUPPORT_CHAT}"
                    )
                ]
            ]
        ),
    )


BUTTON = [
    [
        InlineKeyboardButton(
            "نوێکارییەکانی بۆت 🍻", url=f"https://t.me/{SUPPORT_CHAT}"
        )
    ]
]
CUTIE = "https://64.media.tumblr.com/d701f53eb5681e87a957a547980371d2/tumblr_nbjmdrQyje1qa94xto1_500.gif"


@app.on_message(
    filters.command(
        ["cute", "کیوت", "كیوت", "قشت", "قشتی"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
)
async def cute(_, message):
    if not message.reply_to_message:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
    else:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.first_name

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    CUTE = f"**🍓 {mention}\nڕێژەی قشتیت {mm}% 🥺🫶🏻**"

    await app.send_document(
        chat_id=message.chat.id,
        document=CUTIE,
        caption=CUTE,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=(
            message.reply_to_message.message_id if message.reply_to_message else None
        ),
    )


@app.on_message(
    filters.command(
        ["true", "ڕاستە", "دروستە", "راستە"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
)
async def true_or_false(_, message):
    if not message.text or len(message.command) < 2:
        await message.reply("**تکایە داواکە یان پرسیارەکەت بنووسە پاش فەرمانەکە 🤔**")
        return

    # Get the statement after the command
    text = message.text.split(None, 1)[1]
    true_percentage = random.randint(0, 100)  # Generate a random percentage

    # Define random texts for true and false
    true_responses = [
        "بەڵی، ڕاستە بە ڕێژەی % 😊",
        "ڕاستە بەڵام بێ زانیاری زیاتر % 😌",
        "واو بژی ڕاستە % 🫨",
        "ئەیەباا زۆرر ڕاستە % 🫶🏻",
    ]
    false_responses = [
        "باوکەڕۆ بۆ ئەوەنە درۆزنی % 😅",
        "دڵخۆش مەبە، درۆزن % 😞",
        "ئەمە چاوەڕوان ناکرێت، درۆیە % 🙅",
        "پەکوف لەو درۆیە % 😐",
        "کوڕم ئەتو درۆزن نیت، درۆزانی % 😂🙂",
    ]

    # Determine the result and pick a random response
    if true_percentage > 50:
        is_true = random.choice(true_responses).replace("%", f"{true_percentage}%")
    else:
        is_true = random.choice(false_responses).replace("%", f"{true_percentage}%")

    response = f"<b><blockquote>🙋🏻‍♀ پرسیار: {text}</blockquote></b>\n\n"
    response += f"<b><blockquote>🔮 ئەنجام: {is_true}</blockquote></b>"

    # Reply directly to the message the user is responding to
    await message.reply(
        text=response,
        reply_markup=InlineKeyboardMarkup(BUTTON),
    )

help_text = """
» ᴡʜᴀᴛ ɪꜱ ᴛʜɪꜱ (ᴡɪꜱʜ):
ʏᴏᴜ ʜᴀᴠɪɴɢ ᴀɴʏ ᴋɪɴᴅ ᴏꜰ
(ᴡɪꜱʜᴇꜱ) ʏᴏᴜ ᴄᴀɴ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ ᴛᴏ ʜᴏᴡ ᴘᴏꜱꜱɪʙʟᴇ ᴛᴏ ʏᴏᴜʀ ᴡɪꜱʜ!
ᴇxᴀᴍᴘʟᴇ:» /wish : ɪ ᴡᴀɴᴛ ᴄʟᴀꜱꜱ ᴛᴏᴘᴘᴇʀ
» /wish : ɪ ᴡᴀɴᴛ ᴀ ɴᴇᴡ ɪᴘʜᴏɴᴇ
» /cute : ʜᴏᴡ ᴍᴜᴄʜ ɪ ᴀᴍ ᴄᴜᴛᴇ
"""
