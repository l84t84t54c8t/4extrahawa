import requests
from AlinaMusic import app
from pyrogram import filters

# Regex pattern to match Instagram URLs
instagram_url_pattern = r"(https?://(?:www\.)?instagram\.com/[-a-zA-Z0-9@:%._\+~#=]{2,256}/[-a-zA-Z0-9@:%._\+~#=]+)"


@app.on_message(filters.regex(instagram_url_pattern))
async def down(app, message):
    try:
        link = message.text.strip()
        json_data = {"url": link}
        
        # Send POST request to download Instagram video
        response = requests.post(
            "https://insta.savetube.me/downloadPostVideo", json=json_data
        ).json()

        # Extract video and thumbnail details
        thu = response.get("post_video_thumbnail")
        video = response.get("post_video_url")

        if not thu or not video:
            raise ValueError("Invalid response data")

        # Send thumbnail as a photo
        await message.reply_photo(
            thu,
            caption=f"**← کەمێک چاوەڕێ بکە .. ڤیدیۆ دادەبەزێت ...\n⧉• لەلایەن @{app.me.username}**",
        )

        # Send video directly
        caption = f"**✅꒐ بە سەرکەوتوویی داگرترا\n🎸꒐ بۆتی @{app.me.username}**"
        await app.send_video(message.chat.id, video, caption=caption)

    except Exception as e:
        print(f"Error: {e}")
        await message.reply("**لینك هەڵەیە ئەزیزم**")
