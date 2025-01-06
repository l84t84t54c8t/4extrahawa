from AlinaMusic import app
from AlinaMusic.misc import SUDOERS
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import ChatAdminRequired


async def is_admin(client, chat_id, user_id):
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)


# vc on
def require_admin(func):
    async def wrapper(client, message):
        is_bot_admin = await is_admin(
            client, message.chat.id, (await client.get_me()).id
        )
        if not is_bot_admin:
            await message.reply(
                "<b>• بۆ ئەوەی ئەم فەرمانە کاربکات، پێویستە بۆت ئەدمین بێت ⎋</b>"
            )
            return
        await func(client, message)

    return wrapper


@app.on_message(filters.video_chat_started)
@require_admin
async def brah(client, message):
    await message.reply("<b>• ئەدمین تێلی کردەوە وەرن ⎋</b>")


"""
@app.on_message(filters.video_chat_started)
async def brah(client, message):
    try:
        await message.reply("<b>• ئەدمین تێلی کردەوە وەرن ⎋</b>")
    except ChatAdminRequired:
        # Handle the case when the bot is not an admin
        print(f"Error: Bot does not have admin privileges in chat {message.chat.id}")
        await message.reply(
            "<b>• بۆ ئەوەی ئەم فەرمانە کاربکات، پێویستە بۆت ئەدمین بێت ⎋</b>"
        )

"""


@app.on_message(filters.video_chat_ended)
async def brah2(client, message):
    if message.video_chat_ended and message.video_chat_ended.duration:
        da = message.video_chat_ended.duration
        ma = divmod(da, 60)  # minutes and seconds
        ho = divmod(ma[0], 60)  # hours and minutes
        day = divmod(ho[0], 24)  # days and hours

        if da < 60:
            reply_message = f"**🎻┋ تێل کۆتایی پێھات، ماوەکەی {da} چرکە و داخرا ⎋**"
        elif da < 3600:
            reply_message = f"**🎻┋ تێل کۆتایی پێھات، ماوەکەی {ma[0]} خولەك ⎋**"
        elif da < 86400:
            reply_message = f"**🎻┋ تێل کۆتایی پێھات، ماوەکەی {ho[0]} کاتژمێر ⎋**"
        else:
            reply_message = f"**🎻┋ تێل کۆتایی پێھات، ماوەکەی {day[0]} ڕۆژ ⎋**"

        # Check if the bot has admin privileges
        is_bot_admin = await is_admin(
            client, message.chat.id, (await client.get_me()).id
        )
        if not is_bot_admin:
            print(f"Bot lacks admin privileges in chat {message.chat.id}")
            await message.reply(
                "<b>• بۆ ئەوەی ئەم فەرمانە کاربکات، پێویستە بۆت ئەدمین بێت ⎋</b>"
            )
            return

        # Reply if bot has admin privileges
        try:
            await message.reply(reply_message)
        except ChatAdminRequired:
            print(f"Error: Bot still lacks privileges in chat {message.chat.id}")
    else:
        print("No duration available for the video chat.")


@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):
    expression = message.text.split("/math ", 1)[1]
    try:
        result = eval(expression)
        response = f"ᴛʜᴇ ʀᴇsᴜʟᴛ ɪs : {result}"
    except BaseException:
        response = "ɪɴᴠᴀʟɪᴅ ᴇxᴘʀᴇssɪᴏɴ"
    message.reply(response)


###
@app.on_message(filters.command("leavegroup") & SUDOERS)
async def bot_leave(_, message):
    chat_id = message.chat.id
    text = f"**◗⋮◖ بە سەرکەوتوویی لێفت دەکەم گەشەپێدەر**"
    await message.reply_text(text)
    await app.leave_chat(chat_id=chat_id, delete=True)


####


@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(event):
    msg = await event.respond("Searching...")
    async with aiohttp.ClientSession() as session:
        start = 1
        async with session.get(
            f"https://content-customsearch.googleapis.com/customsearch/v1?cx=ec8db9e1f9e41e65e&q={event.text.split()[1]}&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM&start={start}",
            headers={"x-referer": "https://explorer.apis.google.com"},
        ) as r:
            response = await r.json()
            result = ""

            if not response.get("items"):
                return await msg.edit("No results found!")
            for item in response["items"]:
                title = item["title"]
                link = item["link"]
                if "/s" in item["link"]:
                    link = item["link"].replace("/s", "")
                elif re.search(r"\/\d", item["link"]):
                    link = re.sub(r"\/\d", "", item["link"])
                if "?" in link:
                    link = link.split("?")[0]
                if link in result:
                    # remove duplicates
                    continue
                result += f"{title}\n{link}\n\n"
            prev_and_next_btns = [
                Button.inline("▶️Next▶️", data=f"next {start+10} {event.text.split()[1]}")
            ]
            await msg.edit(result, link_preview=False, buttons=prev_and_next_btns)
            await session.close()
