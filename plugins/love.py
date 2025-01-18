import random

from AlinaMusic import app
from pyrogram import filters


def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice(
            [
                "بەداخەوە خۆشەویستی نێوان ئێوە خراپە، ئێوە چاکنابن ئەبێ دەستکاری بکرێن😂🗿",
                "خۆشەویستی نێوان ئێوە وەکو گوڵ گەشە دەکات",
                "ئەمە سەرەتایەکی جوانە بۆ ئێوە، بەردەوام بن",
            ]
        )
    elif love_percentage <= 70:
        return random.choice(
            [
                "پەیوەندییەکی بەهێز هەیە لە نێوانتان، بی کەپڵێنن😂🙂",
                "شەنسی باشت هەیە😂، ڕازی بکە💘",
                "خۆشەویستی نێوانتان جوانە، بەردەوام بە",
            ]
        )
    else:
        return random.choice(
            [
                "واو ئێوە ئەڵێی بۆ یەک دروست کراون 😍❤",
                "پەیوەندی نێوان ئێوە پێکەوە بوونە تاوەکو مردن🖤",
                "بمێنن بۆ یەکدی ئەزیزەکانم‌💘",
            ]
        )


@app.on_message(filters.command("love", prefixes="/"))
async def love_command(client, message):
    command, *args = message.text.split(" ")
    if len(args) >= 2:
        name1 = args[0].strip()
        name2 = args[1].strip()

        love_percentage = random.randint(10, 100)
        love_message = get_random_message(love_percentage)

        response = f"**{name1} + {name2} = {love_percentage}% 💞\n\n{love_message}**"
    else:
        response = "**تکایە دوو ناو بنووسە لە دوای فەرمانی /love**"

    await app.send_message(message.chat.id, response)


__MODULE__ = "Lᴏᴠᴇ"
__HELP__ = """
**ʟᴏᴠᴇ ᴄᴀʟᴄᴜʟᴀᴛᴏʀ:**

• `/love [name1] [name2]`: Cᴀʟᴄᴜʟᴀᴛᴇs ᴛʜᴇ ᴘᴇʀᴄᴇɴᴛᴀɢᴇ ᴏғ ʟᴏᴠᴇ ʙᴇᴛᴡᴇᴇɴ ᴛᴡᴏ ᴘᴇᴏᴘʟᴇ.
"""
