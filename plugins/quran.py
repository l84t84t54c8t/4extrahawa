import json

import requests
from AlinaMusic import app
from AlinaMusic.core.call import Alina
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton as ikb
from pyrogram.types import InlineKeyboardMarkup as ikm


@app.on_message(filters.command(["قورئان", "قورئانی پیرۆز", "/quran"], ""))
async def quran(c, msg):
    quran = json.loads(open("utils/quran.json").read())["s"]
    keyboard = []
    list = []
    for i in range(1, 11):
        if len(list) == 2:
            copy_list = list.copy()
            keyboard.append(copy_list)
            list.clear()
        name = quran[i - 1]["surah"]
        list.append(ikb(name, callback_data=f"play-{i-1}"))
    keyboard.append(list)
    keyboard.append([ikb("• دواتر •", callback_data="next-1")])
    keyboard.append([ikb("نوێکارییەکانی ئەلینا", url=f"https://t.me/MGIMT")])
    video = f"https://telegra.ph/file/39ee458993b40a8a9a9b9.mp4"
    await msg.reply_video(
        video=video,
        caption=f"**◗⋮◖ [⧉• 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝙖𝙬𝙖𝙡 - پەخشی قورئان](t.me/Haawall)\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n◗⋮◖ بەخێربێی ئەزیزم {msg.from_user.mention}\n◗⋮◖ بۆ بەشی پەخشکردنی قورئانی پیرۆز**",
        reply_markup=ikm(keyboard),
    )


@app.on_callback_query(filters.regex("next") & ~BANNED_USERS)
async def next_quran(c, cq):
    data = (cq.data.strip()).split("-")
    number = int(data[1])
    quran = json.loads(open("utils/quran.json").read())["s"]
    keyboard = []
    list = []
    if (number * 10) == 110:
        for i in range(1, 5):
            if len(list) == 2:
                copy_list = list.copy()
                keyboard.append(copy_list)
                list.clear()
            name = quran[(i + (number * 10)) - 1]["surah"]
            list.append(ikb(name, callback_data=f"play-{(i+(number*10))-1}"))
        keyboard.append(list)
        keyboard.append([ikb("• پێشووتر •", callback_data=f"next-{number-1}")])
    elif number == 0:
        for i in range(1, 11):
            if len(list) == 2:
                copy_list = list.copy()
                keyboard.append(copy_list)
                list.clear()
            name = quran[i - 1]["surah"]
            list.append(ikb(name, callback_data=f"play-{i-1}"))
        keyboard.append(list)
        keyboard.append([ikb("• دواتر •", callback_data="next-1")])
    else:
        for i in range(1, 11):
            if len(list) == 2:
                copy_list = list.copy()
                keyboard.append(copy_list)
                list.clear()
            name = quran[(i + (number * 10)) - 1]["surah"]
            list.append(ikb(name, callback_data=f"play-{(i+(number*10))-1}"))
        keyboard.append(list)
        keyboard.append(
            [
                ikb("• پێشووتر •", callback_data=f"next-{number-1}"),
                ikb("• دواتر •", callback_data=f"next-{number+1}"),
            ]
        )
    await cq.edit_message_reply_markup(ikm(keyboard))


@app.on_callback_query(filters.regex("play") & ~BANNED_USERS)
async def show_quran(c, cq):
    data = (cq.data.strip()).split("-")
    number = int(data[1])
    quran = json.loads(open("utils/quran.json").read())["s"]
    keyboard = []
    list = []
    for i in range(0, 10):
        if len(list) == 2:
            copy_list = list.copy()
            keyboard.append(copy_list)
            list.clear()
        name = quran[number]["sounds"][i]["name"]
        list.append(ikb(name, callback_data=f"runq-{number}-{i}"))
    keyboard.append(list)
    if number == 114:
        keyboard.append([ikb("• پێشووتر •", callback_data=f"play-{number-1}")])
    elif number == 0:
        keyboard.append([ikb("• دواتر •", callback_data=f"play-{number+1}")])
    else:
        keyboard.append(
            [
                ikb("• پێشووتر •", callback_data=f"play-{number-1}"),
                ikb("• دواتر •", callback_data=f"play-{number+1}"),
            ]
        )
    name_suarh = quran[number]["surah"]
    await cq.edit_message_text(
        f"**◗⋮◖ سوڕەتی {name_suarh} هەڵبژێردرا\n◗⋮◖ ئێستا قورئان بێژ هەڵبژێرە**",
        reply_markup=ikm(keyboard),
    )


@app.on_callback_query(filters.regex("runq") & ~BANNED_USERS)
async def show_quran(c, cq):
    data = (cq.data.strip()).split("-")
    number = int(data[1])
    i = int(data[2])
    quran = json.loads(open("utils/quran.json").read())["s"]
    name = quran[number]["surah"]
    per_name = quran[number]["sounds"][i]["name"]
    file = requests.get(quran[number]["sounds"][i]["url"]).content
    open(f"{name}.mp3", "wb").write(file)
    await app.send_audio(
        cq.message.chat.id,
        f"{name}.mp3",
        f"**◗⋮◖ سوڕەتی {name}\n◗⋮◖ بە دەنگی {per_name}\n◗⋮◖ گەشەپێدەر : @Hawaallll**",
        reply_markup=ikm([[ikb("• پەخشکردن •", callback_data=f"done-{number}-{i}")]]),
    )


@app.on_callback_query(filters.regex("done") & ~BANNED_USERS)
async def show_quran(c, cq):
    data = (cq.data.strip()).split("-")
    number = int(data[1])
    i = int(data[2])
    quran = json.loads(open("utils/quran.json").read())["s"]
    try:
        await Alina.join_call(
            cq.message.chat.id,
            cq.message.chat.id,
            quran[number]["sounds"][i]["url"],
            video=None,
        )
        await cq.edit_message_reply_markup(
            ikm(
                [
                    [
                        ikb(
                            "• وەستانی کاتی •",
                            callback_data=f"ADMIN Pause|{cq.message.chat.id}",
                        ),
                        ikb(
                            "• دەستپێکردنەوە •",
                            callback_data=f"ADMIN Resume|{cq.message.chat.id}",
                        ),
                    ],
                    [
                        ikb(
                            "• وەستان •",
                            callback_data=f"ADMIN Stop|{cq.message.chat.id}",
                        )
                    ],
                ]
            )
        )
    except BaseException:
        await Alina.skip_stream(cq.message.chat.id, quran[number]["sounds"][i]["url"])
        await cq.edit_message_reply_markup(
            ikm(
                [
                    [
                        ikb(
                            "• وەستانی کاتی •",
                            callback_data=f"ADMIN Pause|{cq.message.chat.id}",
                        ),
                        ikb(
                            "• دەستپێکردنەوە •",
                            callback_data=f"ADMIN Resume|{cq.message.chat.id}",
                        ),
                    ],
                    [
                        ikb(
                            "• وەستان •",
                            callback_data=f"ADMIN Stop|{cq.message.chat.id}",
                        )
                    ],
                ]
            )
        )
