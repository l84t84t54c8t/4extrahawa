import logging

from AlinaMusic import app
from AlinaMusic.misc import SUDOERS
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import ChatAdminRequired

# Set up logging
logging.basicConfig(level=logging.INFO)


# Utility function to check if a user is an admin
async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except Exception as e:
        logging.warning(f"Failed to check admin status: {e}")
        return False


# Decorator to ensure bot is an admin
def require_admin(func):
    async def wrapper(client, message):
        is_bot_admin = await is_admin(
            client, message.chat.id, (await client.get_me()).id
        )
        if not is_bot_admin:
            await message.reply(
                "<b>• بۆ ئەوەی ئەم فەرمانە کاربکات، پێویستە بۆت ئەدمین بێت ⎋</b>"
            )
            return  # Stop execution if not admin
        await func(client, message)

    return wrapper


# Handle when a video chat is started
@app.on_message(filters.video_chat_started)
@require_admin
async def video_chat_started_handler(client, message):
    try:
        await message.reply("<b>• ئەدمین تێلی کردەوە وەرن ⎋</b>")
    except ChatAdminRequired:
        logging.warning(f"Bot lacks admin privileges in chat {message.chat.id}")


@app.on_message(filters.video_chat_ended)
async def video_chat_ended_handler(client, message):
    if message.video_chat_ended and message.video_chat_ended.duration:
        da = message.video_chat_ended.duration
        ma = divmod(da, 60)  # minutes and seconds
        ho = divmod(ma[0], 60)  # hours and minutes
        day = divmod(ho[0], 24)  # days and hours

        # Generate the reply message based on duration
        if da < 60:
            reply_message = f"**🎻┋ تێل کۆتایی پێھات، ماوەکەی {da} چرکە و داخرا ⎋**"
        elif da < 3600:
            reply_message = f"**🎻┋ تێل کۆتایی پێھات، ماوەکەی {ma[0]} خولەك ⎋**"
        elif da < 86400:
            reply_message = f"**🎻┋ تێل کۆتایی پێھات، ماوەکەی {ho[0]} کاتژمێر ⎋**"
        else:
            reply_message = f"**🎻┋ تێل کۆتایی پێھات، ماوەکەی {day[0]} ڕۆژ ⎋**"

        # Check admin privileges before replying
        is_bot_admin = await is_admin(
            client, message.chat.id, (await client.get_me()).id
        )
        if not is_bot_admin:
            logging.warning(f"Bot lacks admin privileges in chat {message.chat.id}")
            await message.reply(
                "<b>• بۆ ئەوەی ئەم فەرمانە کاربکات، پێویستە بۆت ئەدمین بێت ⎋</b>"
            )
            return

        try:
            await message.reply(reply_message)
        except ChatAdminRequired:
            logging.warning(
                f"Bot still lacks admin privileges in chat {message.chat.id}"
            )
    else:
        logging.info("No duration available for the video chat.")


# Math calculation command


@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):
    try:
        expression = message.text.split("/math ", 1)[1]
        result = eval(expression)
        response = f"ᴛʜᴇ ʀᴇsᴜʟᴛ ɪs : {result}"
    except Exception:
        response = "ɪɴᴠᴀʟɪᴅ ᴇxᴘʀᴇssɪᴏɴ"
    message.reply(response)


# Command to leave a group
@app.on_message(filters.command("leavegroup") & SUDOERS)
async def bot_leave_group(client, message):
    chat_id = message.chat.id
    try:
        text = f"**◗⋮◖ بە سەرکەوتوویی لێفت دەکەم گەشەپێدەر**"
        await message.reply_text(text)
        await client.leave_chat(chat_id=chat_id, delete=True)
    except Exception as e:
        logging.error(f"Failed to leave group: {e}")


# Example of handling search (ensure API keys are configured properly)
@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(event):
    msg = await event.respond("Searching...")
    try:
        async with aiohttp.ClientSession() as session:
            start = 1
            async with session.get(
                f"https://content-customsearch.googleapis.com/customsearch/v1"
                f"?cx=your_cx_key&q={event.text.split()[1]}&key=your_api_key&start={start}"
            ) as r:
                response = await r.json()
                if not response.get("items"):
                    return await msg.edit("No results found!")
                result = "\n\n".join(
                    f"{item['title']}\n{item['link']}" for item in response["items"]
                )
                await msg.edit(result, link_preview=False)
    except Exception as e:
        logging.error(f"Search failed: {e}")
        await msg.edit("Search failed!")


# Handle unexpected errors globally
@app.on_message()
async def catch_all(client, message):
    try:
        # Your additional handlers here
        pass
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
