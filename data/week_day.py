import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class WeekDay(SqlAlchemyBase):
    __tablename__ = 'dayofweek'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True, primary_key=True
    )
    name_subject = sqlalchemy.Column(sqlalchemy.String, nullable=False)