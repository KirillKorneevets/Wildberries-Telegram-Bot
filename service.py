from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User


async def save_user(user_id: int, article: int, session: AsyncSession):
    """
    Сохраняет информацию о пользователе в базе данных.
    Если пользователь с указанным user_id и article уже существует, обновляет его подписку на True.
    Если пользователь не существует, создает новую запись.
    """
    try:
        async with session.begin():
            existing_user = await session.execute(
                select(User).where(User.id_tg_bot == user_id, User.article == article)
            )
            existing_user = existing_user.scalar()

            if existing_user:
                existing_user.subscribed = True
            else:
                new_user = User(id_tg_bot=user_id, article=article, subscribed=True)
                session.add(new_user)

            await session.commit()
    except Exception as e:
        print(f"Ошибка при сохранении пользователя: {e}")