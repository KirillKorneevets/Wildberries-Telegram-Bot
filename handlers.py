from aiogram import Router, types, F
from aiogram.filters import CommandStart
from sqlalchemy import select, desc
from sqlalchemy import update

import keyboards as kb
from wildberries_request import get_info
from models import User
from db_config import async_session
from service import save_user


router = Router()



# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    try:
        await message.reply("Выберите действие:", reply_markup=kb.main)
    except Exception as e:
        await handle_error(message, e)

# Обработчик нажатия кнопки "Получить информацию по товару"
@router.message(F.text == "Получить информацию по товару")
async def get_product_info(message: types.Message):
    try:
        await message.reply("Введите артикул товара:")
    except Exception as e:
        await handle_error(message, e)

# Обработчик нажатия кнопки "Получить информацию из БД"
@router.message(F.text == "Получить информацию из БД")
async def get_db_info(message: types.Message):
    try:
        async with async_session() as session:
            recent_entries = await session.execute(
                select(User).order_by(desc(User.created_at)).limit(5)
            )
            recent_entries = recent_entries.scalars().all()

            if len(recent_entries) < 5:
                all_entries = await session.execute(select(User))
                recent_entries = all_entries.scalars().all()

            if recent_entries:
                info_message = "Последние записи из БД:\n"
                for entry in recent_entries:
                    info_message += f"Артикул: {entry.article}, Время запроса: {entry.created_at}, ID пользователя: {entry.id_tg_bot}\n"
                await message.answer(info_message)
            else:
                await message.answer("База данных пуста.")
    except Exception as e:
        await handle_error(message, e)

# Обработчик нажатия кнопки "Остановить уведомления"
@router.message(F.text == "Остановить уведомления")
async def stop_notifications(message: types.Message):
    try:
        user_id = message.from_user.id
        async with async_session() as session:
            async with session.begin():
                await session.execute(
                    update(User).
                    where(User.id_tg_bot == user_id).
                    values(subscribed=False)
                )
                await session.commit()
                await message.answer("Вы успешно остановили уведомления.")
    except Exception as e:
        await handle_error(message, e)

# Обработчик ввода артикула товара пользователем
@router.message(F.text)
async def user_article(message: types.Message):
    try:
        response = message.text
        article = response
        user_id = message.from_user.id
        async with async_session() as session:
            response = message.text
            user_id = message.from_user.id
            product_info = await get_info(response)

        product_info = await get_info(response)
        if product_info:
            article_id = int(article)
            await save_user(user_id, article_id, session)
            formatted_response = (
                f"Название товара - {product_info['name']}\n"
                f"Артикул товара - {product_info['id']}\n"
                f"Цена - {product_info['salePriceU']} руб\n"
                f"Количество товаров на всех складах: {product_info['total_qty']}\n"
                f"Рейтинг товара - {product_info['rating']}\n"
            )
            await message.answer(formatted_response, reply_markup=kb.settings)
        else:
            await message.answer("Не удалось получить информацию о товаре.")
    except Exception as e:
        await handle_error(message, e)

# Обработчик нажатия кнопки "Подписаться"
@router.callback_query(lambda c: c.data == 'subscribe')
async def subscribe_callback(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        async with async_session() as session:
            user = await session.execute(
                update(User).
                where(User.id_tg_bot == user_id).
                values(subscribed=True)
            )
            await session.commit()

        await callback_query.answer("Вы успешно подписались!")
    except Exception as e:
        await handle_error(callback_query.message, e)

# Функция обработки ошибок
async def handle_error(message: types.Message, error: Exception):
    try:
        await message.answer(f"Произошла ошибка: {error}")
    except Exception as e:
        print(f"Ошибка обработки ошибки: {e}")

