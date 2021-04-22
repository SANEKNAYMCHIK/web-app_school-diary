import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class ScheduleOnDay(SqlAlchemyBase):
    __tablename__ = 'scheduleonday'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    day_of_week = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('dayofweek.id')
    )
    subject = sqlalchemy.Column(
        sqlalchemy.String,
        sqlalchemy.ForeignKey('subjects.id')
    )
    schedule_day = orm.relation('Schedule', back_populates='schedule_on_week')
    day_week = orm.relation('WeekDay')
    lesson = orm.relation('Subjects')