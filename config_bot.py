from aiogram import Bot
from config import settings
bot = Bot(token=settings.BOT_TOKEN)

async def send_message_to_tg_admins(message_text: str):
    for admin_tg_id in settings.ADMIN_TG_IDS:
        try:
            await bot.send_message(chat_id=admin_tg_id, text=message_text)
        except:
            # print(f"{admin_tg_id} - не зареган")
            continue