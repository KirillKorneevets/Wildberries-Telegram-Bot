from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Получить информацию по товару")],
    [KeyboardButton(text="Остановить уведомления")],
    [KeyboardButton(text="Получить информацию из БД")],
])


settings = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='подписаться', callback_data='subscribe')]])