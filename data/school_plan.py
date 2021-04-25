import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm


class SchoolPlan(SqlAlchemyBase, UserMixin):
    __tablename__ = 'schoolplan'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_subject = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('subjects.id')
    )
    id_teacher = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('teacher.id')
    )
    name_subject = orm.relation('Subjects')
    teacher_id_orm = orm.relation('Teacher')