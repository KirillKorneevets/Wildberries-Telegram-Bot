import asyncio
from sqlalchemy import select

from aiogram import Bot
import keyboards as kb
from wildberries_request import get_info
from models import User
from db_config import async_session


async def subscribed_task(bot: Bot):
    """
    Асинхронная задача, которая периодически отправляет уведомления подписанным пользователям.
    Проверяет базу данных на наличие подписанных пользователей и отправляет им информацию по артикулам товаров.
    """
    while True:
        try:
            await asyncio.sleep(300)  

            async with async_session() as session:
                async with session.begin():
                    subscribed_users = await session.execute(
                        select(User).where(User.subscribed == True)
                    )
                    subscribed_users = subscribed_users.scalars().all()

                    for user in subscribed_users:
                        user_id = user.id_tg_bot
                        article_number = user.article

                        product_info = await get_info(article_number)

                        if product_info:
                            formatted_response = (
                                f"Название товара - {product_info['name']}\n"
                                f"Артикул товара - {product_info['id']}\n"
                                f"Цена - {product_info['salePriceU']} руб\n"
                                f"Количество товаров на всех складах: {product_info['total_qty']}\n"
                                f"Рейтинг товара - {product_info['rating']}\n"
                            )
                            await bot.send_message(user_id, formatted_response, reply_markup=kb.settings)
                        else:
                            await bot.send_message(user_id, "Не удалось получить информацию о товаре.")
        except Exception as e:
            print(f"Произошла ошибка во время выполнения задачи: {e}")