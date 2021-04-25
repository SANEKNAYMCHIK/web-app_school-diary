import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Subjects(SqlAlchemyBase):
    __tablename__ = 'subjects'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    id_lesson = orm.relation('SchoolPlan', back_populates='name_subject')
    id_subject = orm.relation('Progress', back_populates='lesson')