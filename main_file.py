from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.input_data import InputData
from data.pupil import Pupil
from data.classes import Class
from data.teacher import Teacher
from data.subjects import Subjects
from data.school_plan import SchoolPlan
from data.schedule import Schedule
from data.progress import Progress
import datetime
from forms.user import RegisterForm, LoginForm, AddModerator, AddTeacher, \
    AddPupil, AddClass, AddSubject, Tabletime, AddTabletimeSubjects, ViewTableTime, ViewModerator, ViewTeacher,\
    ViewPupil, ChangePerson, ViewClass, Back, LessonsChoiceClass, Grades

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    return db_sess.query(InputData).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_sess.expire_on_commit = False
        if db_sess.query(InputData).filter(InputData.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = InputData(
            login=form.login.data,
            level_of_access=2
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_sess.expire_on_commit = False
        user = db_sess.query(InputData).filter(InputData.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/login")
        return render_template('login_2.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_2.html', title='Авторизация', form=form)


@app.route('/addmoder', methods=['GET', 'POST'])
@login_required
def add_moder():
    form = AddModerator()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_sess.expire_on_commit = False
        if db_sess.query(InputData).filter(InputData.login == form.login.data).first():
            return render_template('add_moderator.html', title='Добавление модератора',
                                   form=form,
                                   message="Такой логин уже есть!")
        user = InputData(
            login=form.login.data,
            level_of_access=2
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/addmoder')
    return render_template('add_moderator.html', title='Регистрация', form=form)


@app.route('/viewmoder', methods=['GET', 'POST'])
@login_required
def view_moder():
    form = ViewModerator()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    moders = db_sess.query(InputData).filter(InputData.level_of_access == 2).all()
    if form.validate_on_submit():
        if form.sort_by.data == '1':
            moders_2 = []
            for elem in moders:
                moders_2.append([elem.login, elem.password])
            return render_template('view_moder.html', title='Просмотр и редактирование списка модераторов', form=form, moders=sorted(moders_2, key=lambda x: x[0]), sort=1)
    return render_template('view_moder.html', title='Просмотр и редактирование списка модераторов', form=form, moders=moders)


@app.route('/deletemoder/<login>', methods=['GET', 'POST'])
@login_required
def delete_moder(login):
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    moder = db_sess.query(InputData).filter(InputData.login == login).first()
    db_sess.delete(moder)
    db_sess.commit()
    return redirect('/viewmoder')


@app.route('/addteacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    form = AddTeacher()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    subjects = db_sess.query(Subjects).all()
    list_subjects = [(i.id, i.subject) for i in subjects]
    form.subjects.choices = list_subjects
    if form.validate_on_submit():
        if db_sess.query(InputData).filter(InputData.login == form.login.data).first():
            return render_template('add_teacher.html', title='Добавление учителя',
                                   form=form,
                                   message="Такой логин уже есть!")
        user = InputData(
            login=form.login.data,
            level_of_access=1
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        id = db_sess.query(InputData).filter(InputData.login == form.login.data).first().id
        user = Teacher(
            name=form.name.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data,
            login_password=id
        )
        db_sess.add(user)
        db_sess.commit()
        id_of_teacher = db_sess.query(Teacher).filter(Teacher.login_password == id).first().id
        for i in form.subjects.data:
            data = SchoolPlan(
                id_subject=i,
                id_teacher=id_of_teacher
            )
            db_sess.add(data)
            db_sess.commit()
        return redirect('/addteacher')
    return render_template('add_teacher.html', title='Добавление ученика', form=form)


@app.route('/viewteacher', methods=['GET', 'POST'])
@login_required
def view_teacher():
    form = ViewTeacher()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    teachers = db_sess.query(Teacher).all()
    if form.validate_on_submit():
        teachers_2 = []
        for elem in teachers:
            teachers_2.append([elem.surname, elem.name, elem.patronymic, elem.input_data_orm.login, elem.input_data_orm.password])
        if form.sort_by.data == '1':
            return render_template('view_teacher.html', title='Просмотр и редактирование списка учителей', form=form, teachers=sorted(teachers_2, key=lambda x: x[0]))
        elif form.sort_by.data == '2':
            return render_template('view_teacher.html', title='Просмотр и редактирование списка учителей', form=form, teachers=sorted(teachers_2, key=lambda x: x[1]))
        elif form.sort_by.data == '3':
            return render_template('view_teacher.html', title='Просмотр и редактирование списка учителей', form=form, teachers=sorted(teachers_2, key=lambda x: x[2]))
        return render_template('view_teacher.html', title='Просмотр и редактирование списка учителей', form=form, teachers=teachers)
    return render_template('view_teacher.html', title='Просмотр и редактирование списка учителей', form=form, teachers=teachers, sort=1)


@app.route('/changeteacher/<login>', methods=['GET', 'POST'])
@login_required
def change_teacher(login):
    form = ChangePerson()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    teacher = db_sess.query(InputData).filter(InputData.login == login).first().input_data_teacher[0]
    if form.validate_on_submit():
        if form.type.data == '1':
            teacher.surname = form.value.data
        elif form.type.data == '2':
            teacher.name = form.value.data
        elif form.type.data == '3':
            teacher.patronymic = form.value.data
        db_sess.commit()
    return render_template('change_teacher.html', title='Изменение данных учителя', form=form)


@app.route('/deleteteacher/<login>', methods=['GET', 'POST'])
@login_required
def delete_teacher(login):
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    teacher = db_sess.query(InputData).filter(InputData.login == login).first().input_data_teacher[0]
    lessons = db_sess.query(SchoolPlan).filter(SchoolPlan.id_teacher == teacher.id).all()
    for i in lessons:
        db_sess.delete(i)
        db_sess.commit()
    db_sess.delete(teacher)
    db_sess.commit()
    inp_data = db_sess.query(InputData).filter(InputData.login == login).first()
    db_sess.delete(inp_data)
    db_sess.commit()
    return redirect('/viewteacher')


@app.route('/addpupil', methods=['GET', 'POST'])
@login_required
def add_pupil():
    form = AddPupil()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    classes = db_sess.query(Class).all()
    list_classes = [(i.id, i.name_class) for i in classes]
    form.id_class.choices = list_classes
    if form.validate_on_submit():
        if db_sess.query(InputData).filter(InputData.login == form.login.data).first():
            return render_template('add_pupil.html', title='Добавление ученика',
                                   form=form,
                                   message="Такой логин уже есть!")
        user = InputData(
            login=form.login.data,
            level_of_access=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        id = db_sess.query(InputData).filter(InputData.login == form.login.data).first().id
        user = Pupil(
            name=form.name.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data,
            id_class=form.id_class.data,
            login_password=id,
            schedule=form.id_class.data
        )
        db_sess.add(user)
        db_sess.commit()
        '''teachers = db_sess.query(Class).filter(Class.id == form.id_class.data).first().teacher
        for elem in teachers.split():
            lesson = db_sess.query(SchoolPlan).filter(SchoolPlan.id_teacher == elem).all()
            for i in lesson:
                values = Progress(
                    id_subject=i.name_subject,

                )'''
        return redirect('/addpupil')
    return render_template('add_pupil.html', title='Добавление ученика', form=form)


@app.route('/viewpupil', methods=['GET', 'POST'])
@login_required
def view_pupil():
    form = ViewPupil()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    pupils = db_sess.query(Pupil).all()
    if form.validate_on_submit():
        pupils_2 = []
        for elem in pupils:
            pupils_2.append([elem.surname, elem.name, elem.patronymic, elem.name_class_orm.name_class, elem.input_data_orm.login, elem.input_data_orm.password])
        if form.sort_by.data == '1':
            return render_template('view_pupil.html', title='Просмотр и редактирование списка учащихся', form=form, pupils=sorted(pupils_2, key=lambda x: x[1]))
        elif form.sort_by.data == '2':
            return render_template('view_pupil.html', title='Просмотр и редактирование списка учащихся', form=form, pupils=sorted(pupils_2, key=lambda x: x[0]))
        elif form.sort_by.data == '3':
            return render_template('view_pupil.html', title='Просмотр и редактирование списка учащихся', form=form, pupils=sorted(pupils_2, key=lambda x: x[2]))
        return render_template('view_pupil.html', title='Просмотр и редактирование списка учащихся', form=form, pupils=pupils)
    return render_template('view_pupil.html', title='Просмотр и редактирование списка учащихся', form=form, pupils=pupils, sort=1)


@app.route('/changepupil/<login>', methods=['GET', 'POST'])
@login_required
def change_pupil(login):
    form = ChangePerson()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    pupil = db_sess.query(InputData).filter(InputData.login == login).first().input_data_pupil[0]
    if form.validate_on_submit():
        if form.type.data == '1':
            pupil.surname = form.value.data
        elif form.type.data == '2':
            pupil.name = form.value.data
        elif form.type.data == '3':
            pupil.patronymic = form.value.data
        db_sess.commit()
    return render_template('change_pupil.html', title='Изменение данных ученика', form=form)


@app.route('/deletepupil/<login>', methods=['GET', 'POST'])
@login_required
def delete_pupil(login):
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    pupil = db_sess.query(InputData).filter(InputData.login == login).first().input_data_pupil[0]
    progress = db_sess.query(Progress).filter(Progress.id_pupil == pupil.id).all()
    for elem in progress:
        db_sess.delete(elem)
        db_sess.commit()
    db_sess.delete(pupil)
    db_sess.commit()
    inp_data = db_sess.query(InputData).filter(InputData.login == login).first()
    db_sess.delete(inp_data)
    db_sess.commit()
    return redirect('/viewpupil')


@app.route('/addclass', methods=['GET', 'POST'])
@login_required
def add_class():
    form = AddClass()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    teachers = db_sess.query(SchoolPlan).all()
    list_teachers = [(i.id_teacher, i.teacher_id_orm.surname + ' ' +
                      i.teacher_id_orm.name + ' ' +
                      i.teacher_id_orm.patronymic + ' - ' + i.name_subject.subject) for i in teachers]
    form.teachers.choices = list_teachers
    if form.validate_on_submit():
        if db_sess.query(Class).filter(Class.name_class == form.name_class.data).first():
            return render_template('add_class.html', title='Добавление класса',
                                   form=form,
                                   message="Такой класс уже есть!")
        list_teachers = ''
        for i in form.teachers.data:
            list_teachers += str(i) + ' '
        user = Class(
            name_class=form.name_class.data,
            teacher=list_teachers
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/addclass')
    return render_template('add_class.html', title='Добавление класса', form=form)


@app.route('/viewclass', methods=['GET', 'POST'])
@login_required
def view_class():
    form = ViewClass()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    classes = db_sess.query(Class).all()
    if form.validate_on_submit():
        classes_2 = []
        for elem in classes:
            classes_2.append(elem.name_class)
        if form.sort_by.data == '1':
            return render_template('view_class.html', title='Просмотр классов', form=form,
                                   classes=sorted(classes_2))
        elif form.sort_by.data == '2':
            return render_template('view_class.html', title='Просмотр классов', form=form,
                                   classes=sorted(classes_2, reverse=True))
        return render_template('view_class.html', title='Просмотр классов', form=form,
                               classes=classes)
    return render_template('view_class.html', title='Просмотр классов', form=form,
                           classes=classes, sort=1)


@app.route('/deleteclass/<name>', methods=['GET', 'POST'])
@login_required
def delete_class(name):
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    class_ = db_sess.query(Class).filter(Class.name_class == name).first()
    ind_class = class_.id
    for i in db_sess.query(Pupil).filter(Pupil.id_class == ind_class).all():
        db_sess.delete(i.input_data_orm)
        for j in db_sess.query(Progress).filter(Progress.id_pupil == i.id).all():
            db_sess.delete(j)
        db_sess.delete(i)
        db_sess.commit()
    schedule = db_sess.query(Schedule).filter(Schedule.name_class == ind_class).first()
    db_sess.delete(schedule)
    db_sess.commit()
    db_sess.delete(class_)
    db_sess.commit()
    return redirect('/viewclass')




@app.route('/addsubject', methods=['GET', 'POST'])
@login_required
def add_subject():
    form = AddSubject()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_sess.expire_on_commit = False
        if db_sess.query(Subjects).filter(Subjects.subject == form.name.data).first():
            return render_template('add_subject.html', title='Добавление предмета',
                                   form=form,
                                   message="Такой предмет уже есть!")
        user = Subjects(
            subject=form.name.data
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/addsubject')
    return render_template('add_subject.html', title='Добавление предмета', form=form)


@app.route('/viewsubject', methods=['GET', 'POST'])
@login_required
def view_subject():
    form = Back()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    subjects = db_sess.query(Subjects).all()
    subj_2 = []
    for i in subjects:
        teacher = ''
        for j in i.id_lesson:
            teacher += j.teacher_id_orm.surname + ' ' + j.teacher_id_orm.name + ' ' + j.teacher_id_orm.patronymic + ', '
        if len(teacher) > 0:
            if teacher[-2:] == ', ':
                teacher = teacher[:-2]
        else:
            teacher += 'Учителя нет'
        subj_2.append([i.subject, teacher])
    if form.validate_on_submit():
        return redirect('/')
    return render_template('view_subject.html', title='Просмотр предметов', form=form,
                           subjects=sorted(subj_2, key=lambda x: x[0]))


@app.route('/addtabletime', methods=['GET', 'POST'])
@login_required
def add_tabletime():
    form = Tabletime()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    classes = db_sess.query(Class).all()
    list_classes = [(i.id, i.name_class) for i in classes]
    form.class_.choices = list_classes
    if form.validate_on_submit():
        if form.button_1.data:
            return redirect('/addtabletimday/' + str(form.class_.data) + '/1')
        elif form.button_2.data:
            return redirect('/addtabletimday/' + str(form.class_.data) + '/2')
        elif form.button_3.data:
            return redirect('/addtabletimday/' + str(form.class_.data) + '/3')
        elif form.button_4.data:
            return redirect('/addtabletimday/' + str(form.class_.data) + '/4')
        elif form.button_5.data:
            return redirect('/addtabletimday/' + str(form.class_.data) + '/5')
        elif form.button_6.data:
            return redirect('/addtabletimday/' + str(form.class_.data) + '/6')
        return redirect('/addtabletime')
    return render_template('add_tabletime.html', title='Добавление расписания', form=form)


@app.route('/addtabletimday/<class_>/<numb>', methods=['GET', 'POST'])
@login_required
def add_tabletime_day(class_, numb):
    form = AddTabletimeSubjects()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    subjects = db_sess.query(Subjects).all()
    list_subjects = [(i.id, i.subject) for i in subjects]
    form.subject_1.choices = list_subjects
    form.subject_2.choices = list_subjects
    form.subject_3.choices = list_subjects
    form.subject_4.choices = list_subjects
    form.subject_5.choices = list_subjects
    form.subject_6.choices = list_subjects
    if form.validate_on_submit():
        list_subjects = ''
        list_subjects += str(form.subject_1.data) + ' '
        list_subjects += str(form.subject_2.data) + ' '
        list_subjects += str(form.subject_3.data) + ' '
        list_subjects += str(form.subject_4.data) + ' '
        list_subjects += str(form.subject_5.data) + ' '
        list_subjects += str(form.subject_6.data)
        day_schedule = str(numb) + list_subjects
        if db_sess.query(Schedule).filter(Schedule.name_class == class_).first():
            list_subj = ''
            flag = True
            for i in db_sess.query(Schedule).filter(Schedule.name_class == class_).first().schedule.split(','):
                if int(i[0]) == int(numb):
                    list_subj += day_schedule + ','
                    flag = False
                else:
                    list_subj += i + ','
            if flag:
                list_subj += day_schedule + ','
            if list_subj[-1] == ',':
                list_subj = list_subj[:-1]
            db_sess.query(Schedule).filter(Schedule.name_class == class_).first().schedule = list_subj
            db_sess.commit()
        else:
            user = Schedule(
                name_class=class_,
                schedule=day_schedule
            )
            db_sess.add(user)
            db_sess.commit()
        return redirect('/addtabletime')
    return render_template('add_tabletime_subject.html', title='Добавление расписания', form=form)


@app.route('/viewtabletime', methods=['GET', 'POST'])
@login_required
def view_tabletime_day():
    form = ViewTableTime()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    class_ = db_sess.query(Class).all()
    list_class_ = [(i.id, i.name_class) for i in class_]
    form.class_.choices = list_class_
    if form.validate_on_submit():
        lessons = db_sess.query(Schedule).filter(Schedule.name_class == form.class_.data).first().schedule
        teachers = db_sess.query(Class).filter(Class.id == form.class_.data).first().teacher
        subjects = {}
        for i in teachers.split():
            subj = db_sess.query(SchoolPlan).filter(SchoolPlan.id_teacher == int(i)).all()
            for j in subj:
                if j.id_subject not in subjects:
                    subjects[
                        j.id_subject] = j.teacher_id_orm.surname + ' ' + j.teacher_id_orm.name + ' ' + j.teacher_id_orm.patronymic
        mon = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
               ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
               ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
        thur = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
                ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
                ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
        wedn = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
                ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
                ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
        tues = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
                ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
                ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
        fri = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
               ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
               ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
        sat = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
               ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
               ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
        for j in lessons.split(','):
            day = j[0]
            counter = -1
            for k in j[1:].split():
                counter += 1
                if int(k) in subjects.keys():
                    if int(day) == 1:
                        mon[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                        subjects[int(k)]]
                    elif int(day) == 2:
                        thur[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                         subjects[int(k)]]
                    elif int(day) == 3:
                        wedn[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                         subjects[int(k)]]
                    elif int(day) == 4:
                        tues[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                         subjects[int(k)]]
                    elif int(day) == 5:
                        fri[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                        subjects[int(k)]]
                    elif int(day) == 6:
                        sat[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                        subjects[int(k)]]
        return render_template('view_tabletime.html', title='Просмотр расписания', form=form, flag=True,
                                       mon=mon, thur=thur, wedn=wedn, tues=tues, fri=fri, sat=sat)
    return render_template('view_tabletime.html', title='Просмотр расписания', form=form, flag=False)


@app.route('/lessonsteacher', methods=['GET', 'POST'])
@login_required
def lessons():
    form = LessonsChoiceClass()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    classes = db_sess.query(Class).all()
    classes_2 = [(i.id, i.name_class) for i in classes]
    form.class_.choices = classes_2
    subjects = db_sess.query(SchoolPlan).filter(SchoolPlan.id_teacher == current_user.input_data_teacher[0].id).all()
    subjects_2 = [(i.name_subject.id, i.name_subject.subject) for i in subjects]
    form.subject.choices = subjects_2
    if form.submit.data:
        class_ = db_sess.query(Class).filter(Class.id == form.class_.data).first().name_class
        lesson = db_sess.query(Subjects).filter(Subjects.id == form.subject.data).first().subject
        pupils = db_sess.query(Pupil).filter(Pupil.id_class == form.class_.data).all()
        pupils_2 = []
        for elem in pupils:
            pupils_2.append((elem.id, elem.surname + ' ' + elem.name + ' ' + elem.patronymic))
        days = db_sess.query(Schedule).filter(Schedule.name_class == form.class_.data).first().schedule
        week_day = set()
        week = {
            '1': 'Понедельник',
            '2': 'Вторник',
            '3': 'Среда',
            '4': 'Четверг',
            '5': 'Пятница',
            '6': 'Суббота'
        }
        for i in days.split(','):
            day = i[0]
            for j in i[1:].split():
                if int(j) == form.subject.data:
                    week_day.add((day, week[day]))
        form.pupil.choices = sorted(pupils_2, key=lambda x: x[1])

        return render_template('lesson.html', class_=class_, lesson=lesson, title=class_ + ' ' + lesson,
                                   flag=True, form=form)
    elif form.submit_2.data:
        value = Progress(
            id_pupil=form.pupil.data,
            id_subject=db_sess.query(Subjects).filter(Subjects.id == form.subject.data).first().id,
            date_of_grade=datetime.date.today(),
            grade=form.grade.data
        )
        db_sess.add(value)
        db_sess.commit()
    return render_template('lesson.html', title='Урок', form=form)


@app.route('/classesteacher', methods=['GET', 'POST'])
@login_required
def classes_teacher():
    form = Back()
    if form.back.data:
        return redirect('/')
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    classes = db_sess.query(Class).all()
    classes_2 = set()
    for i in classes:
        for j in i.teacher.split():
            if int(j) == current_user.input_data_teacher[0].id:
                classes_2.add(i.name_class)
    return render_template('classes_teacher.html', title='Просмотр расписания учителя', classes=classes_2, form=form)


@app.route('/tabletimeteacher', methods=['GET', 'POST'])
@login_required
def tabletime_teacher():
    form = Back()
    if form.back.data:
        return redirect('/')
    lessons = []
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    classes = db_sess.query(Class).all()
    subj = db_sess.query(SchoolPlan).filter(SchoolPlan.id_teacher == current_user.input_data_teacher[0].id).all()
    subj_2 = []
    mon = [['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!']]
    thur = [['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!']]
    wedn = [['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!']]
    tues = [['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!']]
    fri = [['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!']]
    sat = [['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!'], ['-', 'Урока нет!']]
    for i in subj:
        subj_2.append(i.id_subject)
    for i in classes:
        for j in i.teacher.split():
            if int(j) == current_user.input_data_teacher[0].id:
                lessons.append(i.id)
    for i in lessons:
        sch = db_sess.query(Schedule).filter(Schedule.name_class == i).first().schedule
        for j in sch.split(','):
            day = j[0]
            counter = -1
            for k in j[1:].split():
                counter += 1
                if int(k) in subj_2:
                    if int(day) == 1:
                        mon[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                        db_sess.query(Class).filter(Class.id == i).first().name_class]
                    elif int(day) == 2:
                        thur[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                        db_sess.query(Class).filter(Class.id == i).first().name_class]
                    elif int(day) == 3:
                        wedn[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                        db_sess.query(Class).filter(Class.id == i).first().name_class]
                    elif int(day) == 4:
                        tues[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                        db_sess.query(Class).filter(Class.id == i).first().name_class]
                    elif int(day) == 5:
                        fri[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                        db_sess.query(Class).filter(Class.id == i).first().name_class]
                    elif int(day) == 6:
                        sat[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject,
                                        db_sess.query(Class).filter(Class.id == i).first().name_class]
    return render_template('tabletime_teacher.html', title='Расписание учителя', form=form, mon=mon, thur=thur,
                               wedn=wedn, tues=tues, fri=fri, sat=sat, flag=True)


@app.route('/tabletimepupil', methods=['GET', 'POST'])
@login_required
def lessons_pupil():
    form = Back()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    if form.back.data:
        return redirect('/')
    lessons = current_user.input_data_pupil[0].schedule_orm.schedule
    teachers = current_user.input_data_pupil[0].schedule_orm.class_name.teacher
    subjects = {}
    for i in teachers.split():
        subj = db_sess.query(SchoolPlan).filter(SchoolPlan.id_teacher == int(i)).all()
        for j in subj:
            if j.id_subject not in subjects:
                subjects[j.id_subject] = j.teacher_id_orm.surname + ' ' + j.teacher_id_orm.name + ' ' + j.teacher_id_orm.patronymic
    mon = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
           ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
    thur = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
            ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
    wedn = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
            ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
    tues = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
            ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
    fri = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
           ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
    sat = [['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!'],
           ['-', 'Урока нет или не назначен учитель!'], ['-', 'Урока нет или не назначен учитель!']]
    for j in lessons.split(','):
        day = j[0]
        counter = -1
        for k in j[1:].split():
            counter += 1
            if int(k) in subjects.keys():
                if int(day) == 1:
                    mon[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject, subjects[int(k)]]
                elif int(day) == 2:
                    thur[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject, subjects[int(k)]]
                elif int(day) == 3:
                    wedn[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject, subjects[int(k)]]
                elif int(day) == 4:
                    tues[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject, subjects[int(k)]]
                elif int(day) == 5:
                    fri[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject, subjects[int(k)]]
                elif int(day) == 6:
                    sat[counter] = [db_sess.query(Subjects).filter(Subjects.id == k).first().subject, subjects[int(k)]]
    return render_template('lessons_pupil.html', title='Расписание ученика', form=form, mon=mon, thur=thur,
                               wedn=wedn, tues=tues, fri=fri, sat=sat, flag=True)


@app.route('/classpupil', methods=['GET', 'POST'])
@login_required
def class_pupil():
    form = Back()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    if form.back.data:
        return redirect('/')
    people = db_sess.query(Pupil).filter(Pupil.id == current_user.input_data_pupil[0].id_class).all()
    people_2 = []
    for i in people:
        people_2.append(i.surname + ' ' + i.name + ' ' + i.patronymic)
    return render_template('classmates.html', title='Одноклассники', form=form, classes=sorted(people_2))


@app.route('/grades', methods=['GET', 'POST'])
@login_required
def grades_pupil():
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    form = Grades()
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    grades = []
    progress_person = db_sess.query(Progress).filter(Progress.id_pupil == current_user.input_data_pupil[0].id_class).all()
    for i in progress_person:
        grades.append([i.lesson.name_subject.subject, i.grade, i.date_of_grade])
    if form.sort_by.data == '1':
        return render_template('grades_pupil.html', title='Оценки', form=form, pupils=sorted(grades, key=lambda x: x[0]))
    elif form.sort_by.data == '2':
        return render_template('grades_pupil.html', title='Оценки', form=form, pupils=sorted(grades, key=lambda x: x[1]))
    elif form.sort_by.data == '3':
        return render_template('grades_pupil.html', title='Оценки', form=form, pupils=sorted(grades, key=lambda x: x[1], reverse=True))
    return render_template('grades_pupil.html', title='Оценки', form=form, sort=1, pupils=progress_person)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


def main():
    db_session.global_init("db/electronic_diary.db")
    app.run()


if __name__ == '__main__':
    main()
