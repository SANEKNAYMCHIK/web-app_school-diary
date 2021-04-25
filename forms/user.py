from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired


class Success(FlaskForm):
    submit = SubmitField('Подтвердить')


class Back(FlaskForm):
    back = SubmitField('Назад')


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class AddPupil(FlaskForm):
    name = StringField('Имя ученика', validators=[DataRequired()])
    surname = StringField('Фамилия ученика', validators=[DataRequired()])
    patronymic = StringField('Отчество ученика', validators=[DataRequired()])
    id_class = SelectField('Класс', coerce=int, validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AddTeacher(FlaskForm):
    name = StringField('Имя учителя', validators=[DataRequired()])
    surname = StringField('Фамилия учителя', validators=[DataRequired()])
    patronymic = StringField('Отчество учителя', validators=[DataRequired()])
    subjects = SelectMultipleField('Предметы', coerce=int, validators=[DataRequired()])
    cab = StringField('Кабинет', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class ViewTeacher(FlaskForm):
    sort_by = SelectField('Сортировать по', choices=[(1, 'Фамилии'), (2, 'Имени'), (3, 'Отчеству')], validators=[DataRequired()])
    submit = SubmitField('Сортировать')


class ViewPupil(FlaskForm):
    sort_by = SelectField('Сортировать по', choices=[(1, 'Фамилии'), (2, 'Имени'), (3, 'Отчеству'), (4, 'Классу')], validators=[DataRequired()])
    submit = SubmitField('Сортировать')


class ViewClass(FlaskForm):
    sort_by = SelectField('Сортировать по', choices=[(1, 'Возрастанию'), (2, 'Убыванию')], validators=[DataRequired()])
    submit = SubmitField('Сортировать')


class ChangeTeacher(FlaskForm):
    type = SelectField('Что изменить?', choices=[(1, 'Фамилия'), (2, 'Имя'), (3, 'Отчество'), (4, 'Кабинет')], validators=[DataRequired()])
    value = StringField("Новые данные", validators=[DataRequired()])
    submit = SubmitField('Изменить')


class ChangePerson(FlaskForm):
    type = SelectField('Что изменить?', choices=[(1, 'Фамилия'), (2, 'Имя'), (3, 'Отчество')], validators=[DataRequired()])
    value = StringField("Новые данные", validators=[DataRequired()])
    submit = SubmitField('Изменить')


class AddModerator(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class ViewModerator(FlaskForm):
    sort_by = SelectField('Сортировать по', choices=[(1, 'Логину')], validators=[DataRequired()])
    submit = SubmitField('Сортировать')


class AddClass(FlaskForm):
    name_class = StringField('Класс (число и буква без пробела)', validators=[DataRequired()])
    teachers = SelectMultipleField('Учителя', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AddSubject(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class Tabletime(FlaskForm):
    class_ = SelectField('Класс', coerce=int, validators=[DataRequired()])
    button_1 = SubmitField('Понедельник')
    button_2 = SubmitField('Вторник')
    button_3 = SubmitField('Среда')
    button_4 = SubmitField('Четверг')
    button_5 = SubmitField('Пятница')
    button_6 = SubmitField('Суббота')


class AddTabletimeSubjects(FlaskForm):
    subject_1 = SelectField('1', coerce=int, validators=[DataRequired()])
    subject_2 = SelectField('2', coerce=int, validators=[DataRequired()])
    subject_3 = SelectField('3', coerce=int, validators=[DataRequired()])
    subject_4 = SelectField('4', coerce=int, validators=[DataRequired()])
    subject_5 = SelectField('5', coerce=int, validators=[DataRequired()])
    subject_6 = SelectField('6', coerce=int, validators=[DataRequired()])
    submit_1 = SubmitField('Добавить')


class ViewTableTime(FlaskForm):
    class_ = SelectField('Выберите класс', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Посмотреть')


class LessonsChoiceClass(FlaskForm):
    class_ = SelectField('Выберите класс', coerce=int, validators=[DataRequired()])
    subject = SelectField('Выберите предмет', coerce=int)
    pupil = SelectField('Ученик', coerce=int, validators=[DataRequired()])
    grade = SelectField('Оценка', choices=[(2), (3), (4), (5)], validators=[DataRequired()])
    class_submit = SubmitField('Выбрать')
    submit = SubmitField('Выбрать')
    submit_2 = SubmitField('Подтвердить')


class Grades(FlaskForm):
    sort_by = SelectField('Сортировать по', choices=[(1, 'Предмету'), (2, 'Оценкам (возрастанию)'),
                                                     (3, 'Оценкам (убыванию)')], validators=[DataRequired()])
    submit = SubmitField('Сортировать')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')