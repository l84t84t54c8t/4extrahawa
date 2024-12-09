import random

from AlinaMusic import app
from config import OWNER_ID
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from strings.filter import command


@app.on_message(command(["گۆرانی"]))
async def music(client: Client, message: Message):
    rl = random.randint(1, 29)
    url = f"https://t.me/ZWZZ7/{rl}"
    await client.send_voice(
        message.chat.id,
        url,
        caption="**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - 🧑🏻‍💻🖤 گۆرانی](t.me/Haawall)**\n\n**••┉┉┉┉┉••🝢••┉┉┉┉┉••**\n**¦  گۆرانییەکانم➧♥️**\n**@Haawall - کەناڵ**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


@app.on_message(command(["وێنە", "وێنەکان"]))
async def ihd(client: Client, message: Message):
    rs = random.randint(1, 148)
    url = f"https://t.me/GTTUTY/{rs}"
    await client.send_photo(
        message.chat.id,
        url,
        caption="**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - 🧑🏻‍💻🖤 وێنەکان](t.me/Haawall)**\n**••┉┉┉┉┉••🝢••┉┉┉┉┉••**\n\n**¦ وێنەکە دیاریکرا ♥•**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


@app.on_message(command(["وێنەی کچان", "کچان"]))
async def ihd(client: Client, message: Message):
    rl = random.randint(1, 45)
    url = f"https://t.me/ZSZZW/{rl}"
    await client.send_photo(
        message.chat.id,
        url,
        caption="**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - 🧑🏻‍💻🖤 کچان](t.me/Haawall)**\n**••┉┉┉┉┉••🝢••┉┉┉┉┉••**\n\n**¦ وێنەی کچان➧♥️\n@Haawall - کەناڵی وێنە**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


@app.on_message(command(["ق"]))
async def voice(client: Client, message: Message):
    rl = random.randint(1, 102)
    url = f"https://t.me/IQQUR/{rl}"
    await client.send_voice(
        message.chat.id,
        url,
        caption="**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - 🧑🏻‍💻🖤 قورئان](t.me/Haawall)**\n**••┉┉┉┉┉••🝢••┉┉┉┉┉••**\n\n**¦ قورئانی پیرۆز➧♥️\n@Haawall - کەناڵی قورئان**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


@app.on_message(command([f"ڤیدیۆ", "v", "ڤ"]))
async def video(client: Client, message: Message):
    rl = random.randint(5, 32)
    u = await client.get_messages("IQVIDE", rl)
    if u.video:
        await client.send_video(
            message.chat.id,
            u.video.file_id,
            caption="**[⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - 🧑🏻‍💻🖤 ڤیدیۆ](t.me/Haawall)**\n**••┉┉┉┉┉••🝢••┉┉┉┉┉••**\n\n**¦ @Haawall - کەناڵی ڤیدیۆ♥️•**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            message.from_user.first_name,
                            url=f"https://t.me/{message.from_user.username}",
                        )
                    ],
                ]
            ),
        )


@app.on_message(command(["ڕۆڵم"]) & filters.group)
async def rotba(client, message):
    dev = OWNER_ID
    haya = (833360381, 1818734394)
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    if message.from_user.id in haya:
        rotba = "پڕۆگرامساز"
    elif message.from_user.id in dev:
        rotba = "خاوەنی بۆت"
    elif get.status in [ChatMemberStatus.ADMINISTRATOR]:
        rotba = "ئەدمین"
    elif get.status in [ChatMemberStatus.OWNER]:
        rotba = "سەرۆك"
    else:
        rotba = "ئەندام"
    await message.reply_text(f"**ڕۆڵی تۆیە لەم گرووپە\n\nڕۆڵت ← « {rotba} »♥️**")


bio = []


@app.on_message(command(["بایۆ"]) & filters.group)
async def idjjdd(client, message: Message):
    if message.chat.id in bio:
        return
    usr = await client.get_chat(message.from_user.id)
    await message.reply_text(f"**ئەوە بایۆیی تۆیە\n│ \n└ʙʏ: {usr.bio}**")


@app.on_message(command(["وێنەکەم"]) & filters.group)
async def idjjdd(client, message):
    if message.chat.id in iddof:
        return
    usr = await client.get_chat(message.from_user.id)
    name = usr.first_name
    i = [
        "0",
        "10",
        "15",
        "20",
        "25",
        "30",
        "35",
        "40",
        "45",
        "50",
        "55",
        "60",
        " 66",
        "70",
        "77",
        "80",
        "85",
        "90",
        "99",
        "100",
        "1000",
    ]
    ik = random.choice(i)
    photo = await app.download_media(usr.photo.big_file_id)
    await message.reply_photo(
        photo,
        caption=f"**ڕێژەی جوانیت \n│ \n└ʙʏ: {ik} %😂❤️**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        name, url=f"https://t.me/{message.from_user.username}"
                    )
                ],
            ]
        ),
    )
