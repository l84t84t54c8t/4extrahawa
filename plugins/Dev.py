import os
from asyncio import gather

from AlinaMusic import app
from config import USER_OWNER, OWNER_ID
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from strings.filter import command


@app.on_message(command(["/source", "سۆرس"]))
async def huhh(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://graph.org/file/b4ace5c5aec2901efed59.jpg",
        caption=f"""**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - 🧑🏻‍💻🖤 گەشەپێدەران](t.me/Haawall)**\n••┉┉┉┉┉••🝢••┉┉┉┉┉••\n**بەخێربێی ئەزیزم{message.from_user.mention} بۆ بەشی گەشەپێدەرانی بۆت🕷️•**\n**بۆ هەبوونی هەرکێشە و پرسیارێك پەیوەندی بە گەشەپێدەر بکە لەڕێگای دووگمەکانی خوارەوە♥•**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("H𝐀𝐖𝐀𝐋 ʲ ↱ˡⁱᶠᵉ↰🐍", url=f"https://t.me/Hawaallll"),
                ],
                [
                    InlineKeyboardButton("𐇮 ﮼ﺣ‌ّــەمــە 🇧🇷 𐇮", url=f"https://t.me/IQ7amo"),
                ],
                [
                    InlineKeyboardButton("⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡", url=f"https://t.me/Haawall"),
                ],
                [
                    InlineKeyboardButton(
                        "『گرووپ بۆت』", url=f"https://t.me/piec0flife"
                    ),
                ],
            ]
        ),
    )


@app.on_message(command(["bot", "بۆت", "بوت"]) & filters.group)
async def iqbot(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://graph.org/file/426283f861812c31153d1.jpg",
        caption=f"""**• باشترین بۆتی گۆرانی بۆ کورد**\n\n**• پاراستن و داگرتن و وەڵامدانەوە\n\n**• 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 -› [𝑯𝒂𝒘𝒂𝒍](t.me/Hawaallll)**\n**• 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 -› [𝑺𝒐𝒖𝒓𝒄𝒆 𝑯𝒂𝒘𝒂𝒍](t.me/Haawall)**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("◌sᴏᴜʀᴄᴇ ʜᴀᴡᴀʟ◌", url=f"https://t.me/Haawall"),
                ],
                [
                    InlineKeyboardButton(
                        "• زیادم بکە بۆ گرووپت 🎻",
                        url=f"https://t.me/{app.username}?startgroup=true",
                    ),
                ],
            ]
        ),
    )

@app.on_message(command(["@IQ7amo"]))
async def yas(client, message):

    usr = await client.get_chat("VTVIT")
    name = usr.first_name
    photo = await app.download_media(usr.photo.big_file_id)
    await message.reply_photo(
        photo,
        caption=f"**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - سەرچاوەی هەواڵ 🧑🏻‍💻](t.me/Haawall)\nزانیاری گەشەپێدەری بۆت\n↜︙𝐍𝐀𝐌𝐄 ↬:{name}\n↜︙𝐔𝐒𝐄𝐑 ↬ :@{usr.username}\n↜︙𝐈𝐃 ↬ :`{usr.id}`\n↜︙𝐁𝐈𝐎 ↬: {usr.bio}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(name, url=f"https://t.me/{usr.username}")],
            ]
        ),
    )


@app.on_message(command(["پڕۆگرامساز"]))
async def yas(client, message):
    usr = await client.get_chat("IQ7amo")
    name = usr.first_name
    photo = await app.download_media(usr.photo.big_file_id)
    await message.reply_photo(
        photo,
        caption=f"**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - 🧑🏻‍💻🖤 پڕۆگرامساز](t.me/Haawall)\nزانیاری پڕۆگرامسازی سەرچاوە\n↜︙𝐍𝐀𝐌𝐄 ↬:{name}\n↜︙𝐔𝐒𝐄𝐑 ↬ :@{usr.username}\n↜︙𝐈𝐃 ↬ :`{usr.id}`\n↜︙𝐁𝐈𝐎 ↬: {usr.bio}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(name, url=f"https://t.me/{usr.username}")],
                [
                    InlineKeyboardButton(
                        "🝢 پەیوەندی کردن 🝢", url=f"https://t.me/{usr.username}"
                    ),
                ],
            ]
        ),
    )


@app.on_message(
    command(
        ["سەرۆک", "@IQ7amo", "گەشەپێدەر", "خاوەنی بۆت", "خاوەنی بوت", "dev", "/dev"]
    )
)
async def yas(client, message):
    usr = await client.get_chat(USER_OWNER)
    name = usr.first_name
    photo = await app.download_media(usr.photo.big_file_id)
    await message.reply_photo(
        photo,
        caption=f"**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - 🧑🏻‍💻🖤 خاوەنی بۆت](t.me/Haawall)\nزانیاری خاوەنی بۆت\n↜︙𝐍𝐀𝐌𝐄 ↬:{name}\n↜︙𝐔𝐒𝐄𝐑 ↬ :@{usr.username}\n↜︙𝐈𝐃 ↬ :`{usr.id}`\n↜︙𝐁𝐈𝐎 ↬: {usr.bio}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(name, url=f"https://t.me/{usr.username}")],
                [
                    InlineKeyboardButton(
                        "کەناڵی گەشەپێدەر", url=f"https://t.me/Haawall"
                    ),
                ],
            ]
        ),
    )



@app.on_message(command(["زیرەکی دەستکرد"]))
async def huhh(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/7713aee1676f475d4ed21.jpg",
        caption=f"""**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - زیرەکی دەستکرد🧑🏻‍💻🖤](t.me/Haawall)**\n\n**بەخێربێی ئەزیزم {message.from_user.mention} بۆ بەشی زیرەکی دەستکرد تایبەت بە سەرچاوەی زیرەك**\n** بۆ بەکارهێنانی بنووسە : iq + پرسیارەکەت ♥⚡**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("H𝐀𝐖𝐀𝐋 ʲ ↱ˡⁱᶠᵉ↰🐍", user_id=OWNER_ID),
                ],
                [
                    InlineKeyboardButton("⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡", url=f"https://t.me/Haawall"),
                ],
            ]
        ),
    )


@app.on_message(command(["سەرۆکی گرووپ", "خاوەنی گرووپ", "owner"]) & filters.group)
async def gak_owne(client: Client, message: Message):
    if len(message.command) >= 2:
        return
    else:
        chat_id = message.chat.id

        async for member in client.get_chat_members(chat_id):
            if member.status == ChatMemberStatus.OWNER:
                id = member.user.id
                key = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(member.user.first_name, user_id=id)]]
                )
                m = await client.get_chat(id)
                if m.photo:
                    photo = await app.download_media(m.photo.big_file_id)
                    return await message.reply_photo(
                        photo,
                        caption=f"**✧ ¦زانیاری خاوەن گرووپ \n\n ✧ ¦ ناو ← {m.first_name} \n ✧ ¦ یوزەر ← @{m.username} \n ✧ ¦ بایۆ ← {m.bio}**",
                        reply_markup=key,
                    )
                else:
                    return await message.reply("•" + member.user.mention)


@app.on_message(command(["گرووپ", "group"]) & filters.group)
async def ginnj(client: Client, message: Message):
    chat_idd = message.chat.id
    chat_name = message.chat.title
    chat_username = f"@{message.chat.username}"
    photo = await client.download_media(message.chat.photo.big_file_id)
    await message.reply_photo(
        photo=photo,
        caption=f"""**🦩 ¦ ꪀᥲ️ꪔᥱ » {chat_name}\n🐉 ¦ Ꭵժ ᘜᖇ᥆υρ »  -{chat_idd}\n🐊 ¦ ᥣᎥꪀk » {chat_username}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        chat_name, url=f"https://t.me/{message.chat.username}"
                    )
                ],
            ]
        ),
    )


@app.on_message(command(["گۆڕین", "گۆڕینی ستیکەر"]))
async def sticker_image(client: Client, message: Message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply("**ڕپلەی ستیکەر بکە**")
    if not reply.sticker:
        return await message.reply("**ڕپلەی ستیکەر بکە**")
    m = await message.reply("**کەمێك چاوەڕێبە . .**")
    f = await reply.download(f"{reply.sticker.file_unique_id}.png")
    await gather(*[message.reply_photo(f), message.reply_document(f)])
    await m.delete()
    os.remove(f)


@app.on_message(command(["ناوم", "ناو"]) & filters.group)
async def vgdg(client: Client, message: Message):
    await message.reply_text(f"""•⎆┊** ناوت 🔥♥**»»  {message.from_user.mention()}""")


@app.on_message(filters.command("", "."))
async def vgdg(client, message):
    await message.reply_text(
        f"""**✧ 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖡𝖺𝖻𝗒,
𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 -› [𝑯𝒂𝒘𝒂𝒍 ♪](t.me/Hawaallll)
𝖢𝗁𝖺𝗇𝗇𝖾𝗅 -› [𝑺𝒐𝒖𝒓𝒄𝒆 𝑯𝒂𝒘𝒂𝒍](t.me/Haawall)**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("نوێکارییەکانی هەواڵ 🍻", url=f"t.me/Haawall")]]
        ),
        disable_web_page_preview=True,
    )


@app.on_message(
    command(
        [
            "link delet",
            "لینکی سرینەوە",
            "لینکی سڕینەوە",
            "بەستەری سڕینەوە",
            "سووتاندنی ئەکاونت",
            "سوتاندن",
            "سووتاندن",
        ]
    )
)
async def delet(client: Client, message: Message):
    await message.reply_text(
        f"""**• بەخێربێی ئەزیزم\n-› ئەمانە لینکی سووتاندنی سۆشیاڵ میدیان لەگەڵ بۆتێکی سووتاندنی تێلەگرام**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "• 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 •", url=f"https://my.telegram.org/auth?to=delete"
                    ),
                    InlineKeyboardButton(
                        "• 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖡𝗈𝗍 •", url=f"https://t.me/IQDLBOT"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "• 𝖨𝗇𝗌𝗍𝖺𝗀𝗋𝖺𝗆 •",
                        url=f"https://www.instagram.com/accounts/login/?next=/accounts/remove/request/permanent/",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "• 𝖲𝗇𝖺𝗉𝖢𝗁𝖺𝗍 •",
                        url=f"https://accounts.snapchat.com/accounts/login?continue=https%3A%2F%2Faccounts.snapchat.com%2Faccounts%2Fdeleteaccount",
                    ),
                    InlineKeyboardButton(
                        "• 𝖥𝖺𝖼𝖾𝖡𝗈𝗈𝗄 •",
                        url=f"https://www.faecbook.com/help/deleteaccount",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "• 𝖳𝗐𝗂𝗍𝗍𝖾𝗋 •",
                        url=f"https://mobile.twitter.com/settings/deactivate",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "نوێکارییەکانی هەواڵ 🍻", url=f"https://t.me/Haawall"
                    ),
                ],
            ]
        ),
    )
