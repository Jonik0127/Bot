import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMemberStatus
from aiogram.filters import Command
import os

TOKEN = os.getenv("7497241427:AAEz4dnCDwAVaIo3KldcUad_pHO-LWNh5Pc")
GROUP_ID = int(os.getenv("5916549510"))
ADMIN_ID = int(os.getenv("-1002418748551"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

join_requests = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salom! Guruhga qo‘shilish uchun /join buyrug‘ini bering.")

@dp.message(Command("join"))
async def request_join(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    
    join_requests[user_id] = message.from_user
    
    admin_id = ADMIN_ID
    accept_button = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"accept_{user_id}")
    )
    
    await bot.send_message(admin_id, f"{user_name} ({user_id}) guruhga qo‘shilmoqchi.", reply_markup=accept_button)
    await message.answer("So‘rovingiz yuborildi, admin tasdiqlashini kuting.")

@dp.callback_query(lambda c: c.data.startswith("accept_"))
async def accept_request(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    
    if user_id in join_requests:
        user = join_requests.pop(user_id)
        
        try:
            await bot.approve_chat_join_request(GROUP_ID, user.id)
            await bot.send_message(user.id, "✅ Siz guruhga qo‘shildingiz!")
            await callback_query.answer("Foydalanuvchi guruhga qo‘shildi!", show_alert=True)
        except Exception as e:
            logging.error(e)
            await callback_query.answer("❌ Xatolik yuz berdi!", show_alert=True)
    else:
        await callback_query.answer("Bu so‘rov allaqachon ko‘rib chiqilgan.", show_alert=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
