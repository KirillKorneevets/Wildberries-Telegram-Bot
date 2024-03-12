from sqlalchemy import Column, Integer, DateTime,  MetaData, Boolean

from db_config import AsyncBase


metadata = MetaData()


class User(AsyncBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    id_tg_bot= Column(Integer)
    article = Column(Integer)
    created_at = Column(DateTime)
    subscribed = Column(Boolean, default=False)


