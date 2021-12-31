#-------------------------------------- https://github.com/m4mallu/PMChatbot ------------------------------------------#
import os

from pyrogram import Client, filters
from presets import Presets
if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
ADMINS = int(os.environ.get("ADMINS"))

@Client.on_message(filters.private & filters.text)
async def pm_text(bot, message):
    if message.from_user.id == Config.ADMINS:
        await reply_text(bot, message)
        return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.send_message(
        chat_id=Config.ADMINS,
        text=Presets.PM_TXT_ATT.format(reference_id, info.first_name, message.text),
        parse_mode="html"
    )


@Client.on_message(filters.private & filters.media)
async def pm_media(bot, message):
    if message.from_user.id == Config.ADMINS:
        await replay_media(bot, message)
        return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.copy_message(
        chat_id=Config.ADMINS,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        caption=Presets.PM_MED_ATT.format(reference_id, info.first_name),
        parse_mode="html"
    )


@Client.on_message(filters.user(Config.ADMINS) & filters.text)
async def reply_text(bot, message):
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception:
            pass
        await bot.send_message(
            text=message.text,
            chat_id=int(reference_id)
        )


@Client.on_message(filters.user(Config.ADMINS) & filters.media)
async def replay_media(bot, message):
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception:
            pass
        await bot.copy_message(
            chat_id=int(reference_id),
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            parse_mode="html"
        )
