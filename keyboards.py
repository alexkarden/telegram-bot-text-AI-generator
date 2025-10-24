from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# кнопки
button_end = InlineKeyboardButton(
    text="❌Завершить", callback_data="end"
)

# клавиатуры
keyboard_after_answer = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_end]
    ]
)