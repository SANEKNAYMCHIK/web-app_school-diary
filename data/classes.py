import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Class(SqlAlchemyBase):
    __tablename__ = 'class'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           autoincrement=True, primary_key=True)
    name_class = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    teacher = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name_class_schedule = orm.relation('Schedule',
                                       back_populates='class_name')
    name_class_pupil = orm.relation('Pupil',
                                    back_populates='name_class_orm')