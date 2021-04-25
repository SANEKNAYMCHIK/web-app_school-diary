import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Progress(SqlAlchemyBase):
    __tablename__ = 'progress'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_pupil = sqlalchemy.Column(
        sqlalchemy.Integer
    )
    id_subject = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('subjects.id')
    )
    date_of_grade = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    grade = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    lesson = orm.relation('Subjects')