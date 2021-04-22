import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm


class Pupil(SqlAlchemyBase, UserMixin):
    __tablename__ = 'pupil'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    id_class = sqlalchemy.Column(
        sqlalchemy.String,
        sqlalchemy.ForeignKey('class.id')
    )
    login_password = sqlalchemy.Column(
        sqlalchemy.String,
        sqlalchemy.ForeignKey('input_data.id')
    )
    schedule = sqlalchemy.Column(
        sqlalchemy.String,
        sqlalchemy.ForeignKey('schedule.id')
    )
    name_class_orm = orm.relation('Class')
    input_data_orm = orm.relation('InputData')
    schedule_orm = orm.relation('Schedule')