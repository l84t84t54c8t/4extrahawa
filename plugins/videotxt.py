import os

import speech_recognition as sr
from AlinaMusic import app
from pydub import AudioSegment
from pyrogram import filters
from pyrogram.types import Message


# --------------------------------------


def convert_video_to_text(video_path):
    audio = AudioSegment.from_file(video_path)
    audio.export("audio.wav", format="wav")
    # -----------------------------------------
    recognizer = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio_data = recognizer.record(source)
    # --------------------------------------------
    text = recognizer.recognize_google(audio_data)
    return text


# ----------------------------------------------


@app.on_message(filters.command("vtxt") & filters.reply)
async def convert_video_to_text_cmd(_, message: Message):
    # -------------------------------
    video_path = await message.reply_to_message.download("video.mp4")

    # ------------------------------
    text_result = convert_video_to_text(video_path)

    # --------------------------
    with open("file.txt", "w", encoding="utf-8") as file:
        file.write(text_result)
    # ---------------------------
    await message.reply_document("file.txt")

    # Clean up temporary files
    os.remove("file.txt")
    os.remove(video_path)


@app.on_message(filters.command(["لادانی", "/remove"], "") & filters.reply)
async def remove_media(client, message: Message):
    # Fetching the replied message
    replied_message = message.reply_to_message

    if replied_message.video:
        # If the replied message is a video, remove either the audio or the
        # video
        if len(message.command) > 1:
            command = message.command[1].lower()
            if command in ["video", "ڤیدیۆ", "ڤیدیو"]:
                # Remove audio
                file_path = await app.download_media(replied_message.video)
                audio = AudioSegment.from_file(file_path)
                audio = audio.set_channels(1)
                audio.export("output.mp3", format="mp3")
                await app.send_audio(message.chat.id, "output.mp3")
                os.remove(file_path)
                os.remove("output.mp3")
            elif command in ["audio", "گۆرانی", "دەنگ"]:
                # Remove video
                file_path = await app.download_media(replied_message.video)
                os.system(f"ffmpeg -i {file_path} -c copy -an output.mp4")
                await app.send_video(message.chat.id, "output.mp4")
                os.remove(file_path)
                os.remove("output.mp4")
            else:
                await app.send_message(
                    message.chat.id,
                    "**فەرمانت هەڵە بەکارهێنا بەم شێوازەیە :\nلادانی گۆرانی یان لادانی ڤیدیۆ\n /remove audio یان /remove video**",
                )
        else:
            await app.send_message(
                message.chat.id,
                "**تکایە دیاری بکە کە ئایا دەنگ یان ڤیدیۆ بە بەکارهێنانی /remove audio  /remove video**",
            )
    else:
        await app.send_message(message.chat.id, "**ڕیپلەی ڤیدیۆت نەکردووە**")
