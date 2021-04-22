import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Schedule(SqlAlchemyBase):
    __tablename__ = 'schedule'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name_class = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('class.id')
    )
    schedule = sqlalchemy.Column(
        sqlalchemy.String,
        sqlalchemy.ForeignKey('scheduleonday.id')
    )
    schedule_pupil = orm.relation('Pupil', back_populates='schedule_orm')
    class_name = orm.relation('Class')
    schedule_on_week = orm.relation('ScheduleOnDay')