import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm


class Teacher(SqlAlchemyBase, UserMixin):
    __tablename__ = 'teacher'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    login_password = sqlalchemy.Column(
        sqlalchemy.String,
        sqlalchemy.ForeignKey('input_data.id')
    )
    cabinet = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    id_teacher_lesson = orm.relation('SchoolPlan',
                                     back_populates='teacher_id_orm')
    input_data_orm = orm.relation('InputData')