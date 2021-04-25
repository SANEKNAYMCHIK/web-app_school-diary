import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class InputData(SqlAlchemyBase, UserMixin):
    __tablename__ = 'input_data'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    level_of_access = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    input_data_pupil = orm.relation('Pupil', back_populates='input_data_orm')
    input_data_teacher = orm.relation('Teacher',
                                      back_populates='input_data_orm')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)