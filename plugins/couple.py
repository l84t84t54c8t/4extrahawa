import os
import random

from AlinaMusic import app
from AlinaMusic.core.mongo import mongodb
from config import BANNED_USERS, USER_OWNER
from PIL import Image, ImageDraw
from pyrogram import filters
from pyrogram.enums import ChatAction, ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# MongoDB collection for storing locked permissions
coupledb = mongodb.couple


# Lock state functions for MongoDB
async def update_lock_state(chat_id: int, state: bool):
    """Update the lock state for a specific chat."""
    await coupledb.update_one(
        {"chat_id": chat_id}, {"$set": {"locked": state}}, upsert=True
    )


async def get_lock_state(chat_id: int) -> bool:
    """Retrieve the lock state for a specific chat."""
    chat = await coupledb.find_one({"chat_id": chat_id})
    return chat.get("locked", False) if chat else False


@app.on_message(
    filters.command(
        ["/lock_couples", "/lockkapl", "داخستنی کەپڵ", "داخستنی کەپل"],
        prefixes=["/", "!", "%", ",", "", "@", "#"],
    )
    & ~BANNED_USERS
)
@utils.adminsOnly("can_change_info")
async def lock_couples_command(_, message):
    chat_id = message.chat.id
    if await get_lock_state(chat_id):
        return await message.reply_text("**🔒 فەرمانی کەپڵ پێشتر داخراوە !**")

    await update_lock_state(chat_id, True)
    await message.reply_text("**🔒 فەرمانی کەپڵ داخرا !**")


@app.on_message(
    filters.command(
        ["unlock_couples", "unlockkapl", "کردنەوەی کەپڵ", "کردنەوەی کەپل"],
        prefixes=["/", "!", "%", ",", "", "@", "#"],
    )
    & ~BANNED_USERS
)
@utils.adminsOnly("can_change_info")
async def unlock_couples_command(_, message):
    chat_id = message.chat.id
    if not await get_lock_state(chat_id):
        return await message.reply_text("**🔓 فەرمانی کەپڵ پێشتر کراوەتەوە !**")

    await update_lock_state(chat_id, False)
    await message.reply_text("**🔓 فەرمانی کەپڵ کرایەوە !**")


@app.on_message(
    filters.command(
        ["couples", "couple", "kapl", "قل", "کەپل", "کەپڵ"],
        prefixes=["/", "!", "%", ",", "", "@", "#"],
    )
    & ~BANNED_USERS
)
async def couples(_, message):
    chat_id = message.chat.id

    if await get_lock_state(chat_id):
        return await message.reply_text("**🔒 ببورە ئەم فەرمانە داخراوە**")

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("**تەنیا لە گرووپ کارەکات😂🙂**")

    msg = await message.reply_text("**دوو ئاشقە شێتەکە دیاری دەکرێت😂🙂🫶🏻!**")
    list_of_users = [
        member.user.id
        async for member in app.get_chat_members(chat_id, limit=50)
        if not member.user.is_bot and not member.user.is_deleted
    ]

    if len(list_of_users) < 2:
        return await msg.edit("Not enough members to form a couple! 😢")

    c1_id, c2_id = random.sample(list_of_users, 2)
    user1, user2 = await app.get_users([c1_id, c2_id])
    photo1, photo2 = user1.photo, user2.photo

    # Download profile pictures
    p1 = await app.download_media(photo1.big_file_id) if photo1 else "assets/upic.png"
    p2 = await app.download_media(photo2.big_file_id) if photo2 else "assets/upic.png"

    try:
        img1, img2 = Image.open(p1).resize((437, 437)), Image.open(p2).resize(
            (437, 437)
        )
        mask = Image.new("L", (437, 437), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 437, 437), fill=255)
        img1.putalpha(mask)
        img2.putalpha(mask)

        combined_img = Image.open("assets/cppic.png")
        combined_img.paste(img1, (116, 160), img1)
        combined_img.paste(img2, (789, 160), img2)
        output_path = f"couple_{chat_id}.png"
        combined_img.save(output_path)

        caption = f"""**
کەپڵەکان دیاری کران 💍🌚 :
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
{user1.mention} + {user2.mention} = ❣️
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
پیرۆزە 😂🎉
**"""
        await app.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
        await message.reply_photo(
            output_path,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👻 خاوەنی بۆت 👻", url=f"https://t.me/{USER_OWNER}"
                        )
                    ]
                ]
            ),
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
    finally:
        os.remove(p1) if os.path.exists(p1) else None
        os.remove(p2) if os.path.exists(p2) else None
        os.remove(output_path) if os.path.exists(output_path) else None
        await msg.delete()
