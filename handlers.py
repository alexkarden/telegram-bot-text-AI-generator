import math

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from keyboards import keyboard_after_answer
from script import text_generated


load_dotenv()
router = Router()
global users_dict
users_dict = {}


@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "👋 <b>Добро пожаловать!</b>\n\n"
        "Я могу:\n"
        "-Писать рефераты/рассказы/песни/стихи/статьи на любые темы\n"
        "-Решать математические задачи\n"
        "-Создать резюме\n"
        "-Кодить и обучать кодингу\n"
        "-Объяснить любую тему \n"
        "-Шутить\n\n"
        "Мои возможности ограничены только вашей фантазией.\n\n"
        "Бот помнит Ваши предыдущие сообщения и отвечает, основываясь на них. Если Вы хотите начать чат на новую тему - нажмите кнопку '❌Завершить'\n\n"
        "Напишите, что я могу для вас сделать?"
    )
    await message.answer(f"{welcome_text}", parse_mode=ParseMode.HTML)


# Обрабатываем исключительно текстовые сообщения (чтобы не перехватывать документы/фото)
@router.message(F.content_type == types.ContentType.TEXT)
async def all_message(message: Message):
    await message.answer("Генерируем.....")
    text_message = str(message.text)
    message_dict = {"role": "system", "content": f"{text_message}"}
    if message.from_user.id in users_dict:
        user_list = users_dict[message.from_user.id]
        user_list.append(message_dict)
    else:
        user_message_list = [message_dict]
        users_dict[message.from_user.id] = user_message_list
    message_list = users_dict[message.from_user.id]
    ai_answer = await text_generated(message_list)
    if text_message and ai_answer:
        range_answer = math.ceil(len(ai_answer) / 4096)
        for number in range(range_answer):
            stringtg = ai_answer[number*4096:(number+1)*4096]
            await message.answer(f"{stringtg}", reply_markup=keyboard_after_answer, parse_mode=ParseMode.HTML)
    else:
        await message.answer("'Sad but True' - cервер перегружен, попробуйте позже.")


@router.callback_query()
async def callback_query(callback: CallbackQuery):
    data = callback.data
    if data == "end":
        if callback.from_user.id in users_dict:
            del users_dict[callback.from_user.id]
        await callback.message.answer("Чат очищен! - Можете начать заново" ,parse_mode=ParseMode.HTML)
