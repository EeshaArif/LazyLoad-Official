from flask import Flask, render_template, url_for, flash, redirect, sessions, request
from flask_sqlalchemy import SQLAlchemy
from forms import  LoginForm, MakeAnnouncementForm, AdminLoginForm, TeacherLoginForm, StudentScheduleForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import MenuLink
from flask_admin.actions import action
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required


student_dictionary = {}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hbfrYGBTr7%^R^%*&&**YUR434r656ty55o7o'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
login_manager.login_message_category = 'info'

"""login_manager.login_view = 'teacherlogin'
login_manager.login_message_category = 'info'"""

@login_manager.user_loader
def load_student(student_id):
    return Student.query.get(int(student_id))

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    roll_no = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        student_dictionary[self.name] = self.roll_no
        return f"{self.name},{self.roll_no}"


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"teacher id: {self.username}, password: {self.password}"

"""class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))"""

admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_link(MenuLink(name='Make Announcements', category='Actions', url='/makeannouncement'))
admin.add_link(MenuLink(name='Return Home', category='Actions', url='/home'))

"""class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)"""

"""def __repr__(self):
    return f"admin id: {self.name}, password: {self.password}"""""




@app.route('/')
@app.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/about', methods = ['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(roll_no=form.roll_no.data).first()
        if student and student.password == form.password.data:
            login_user(student, remember=form.remember.data)
            flash(f'You are now Logged in!', 'success')
            return redirect(url_for('account'))
        else:
            flash("Couldn't login, Please check your Roll Number or Password", 'danger')
    return render_template('login.html', form=form)

@app.route('/teacherlogin', methods=['GET', 'POST'])
def teacherlogin():
    form = TeacherLoginForm()
    teacher = Teacher.query.filter_by(username=form.username.data).first()
    if form.validate_on_submit():
        if teacher and teacher.password == form.password.data:
            login_user(teacher, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('teacher'))
        else:
            flash("Couldn't login. Please check username or password", 'danger')
    return render_template('teacherlogin.html', form=form)

@app.route('/adminlogin', methods =['GET', 'POST'])
def adminlogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.admin_id.data == '090078601' and form.password.data == 'niggachu':
            flash('Welcome Admin', 'success')
            return redirect('/admin')
        else:
            flash('Login Unsuccessful. Please check Admin ID or password', 'danger')
    return render_template('adminlogin.html', form=form)

@app.route('/account', methods =['GET', 'POST'])
@login_required
def account():
    return render_template('account.html')

@app.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher():
    return render_template('teacher.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/abdulrafey', methods=['GET', 'POST'])
def abdulrafey():
    return render_template('abdulrafey.html')

@app.route('/hammad', methods=['GET', 'POST'])
def hammad():
    return render_template('hammad.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    return render_template('weekly planner.html')

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    return render_template('courses.html')

###Advisor
@app.route('/advisor', methods=['GET', 'POST'])
@login_required
def advisor():
    l = Student.query.all()
    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)

    form = StudentScheduleForm()
    #for i in student_roll_no_list:
    if form.validate_on_submit():
        rollno=form.roll_no._value()
        wakeupt=form.wakeuptime._value()
        sleep=form.sleeptime._value()
        breakfast=form.breakfasttime._value()
        lunch=form.lunchtime._value()
        dinner=form.dinnertime._value()
        sgoing=form.schoolgoing._value()
        sreturn=form.schoolreturning._value()
        #agoing=form.academygoing._value()
        #areturn=form.academyreturning._value()
        fall_test=form.falltest._value()
        spring_test=form.springtest._value()
        fall_test_percent=(int(fall_test)/50)*100
        spring_test_percent=(int(spring_test)/50)*100
        average=(fall_test_percent+spring_test_percent)/2
        try:
            agoing = form.academygoing._value()
            areturn = form.academyreturning._value()
        except:
            freetime1="{}-{}".format(sreturn,int(dinner))
            freetime2="{}-{}".format(int(dinner)+100,sleep)
        else:
            freetime1 = "{}-{}".format(sreturn, agoing)
            freetime2 = "{}-{}".format(areturn, sleep)

        if average>=80 and average<=90:
            advice="Your Grades are really good but you still need to study!, We recommend you studying for 30 minutes"
        elif average>=70 and average<80:
            advice="Since your grades are good, they can be improved even more!, We recommend you studying for an hour"
        elif average<70:
            advice="Since your Grades aren't satisfactory, We recommend you studying for 2 hours"
        elif average>90:
            advice="Keep up the brilint work!, you don't need an advice, GO PLAY GAMES"
        a = 'Free time: {},{}'.format(freetime1,freetime2)
        if average<90:
            with open('advise.txt', 'w') as f:
                f.write("{}\nAfter thoroughly analyzing your routine, here's a good time to study: {},{}".format(advice, freetime1, freetime2))
        else:
            with open('advise.txt', 'w') as f:
                f.write("{}\n ".format(advice))

        return redirect(url_for('advising'))

    return render_template('studentadvisor.html', form=form)

@app.route('/advising', methods=['GET', 'POST'])
@login_required
def advising():
    with open('advise.txt', 'r') as f:
        a = f.readlines()
        for i in a:
            advise = a[0]
            free_time = a[1]

    return render_template('advising.html', advise=advise, free_time=free_time)




###Announcement

finalmarksdic={}
fallmarksdic={}
springmarksdic={}
@app.route('/makeannouncement',methods = ['GET', 'POST'])
def makeannouncement():
    form=MakeAnnouncementForm()
    if form.validate_on_submit():
        f=open('Title.txt','w')
        f.write(f"{form.title._value()}\n{form.content._value()}")
        #f.write(form.content._value())
        f.close()
        flash(f'Announcement has been successfully made!', 'success')
        return redirect(url_for('home'))
    return render_template('makeannouncement.html', form=form)

@app.route("/announcement")
def announcement():
    f = open("Title.txt", "r")
    title = f.readline()
    content = f.readline()
    f.close()
    return render_template("announce.html", title=title, content=content)

###Enter Results

@app.route("/entertestresults", methods=["GET",'POST'])
def entertestresults():
    return render_template("entertestresults.html")

@app.route("/falltestseries", methods=["GET",'POST'])
@login_required
def falltestseries():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)

    num=len(student_name_list)


    f=open("falltestseries.txt",'w+')
    return render_template("falltestseries.html",num=num, student_name_list=student_name_list, f=f)

@app.route("/springtestseries", methods=["GET",'POST'])
@login_required
def springtestseries():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    return render_template("springtestseries.html",num=num, student_name_list=student_name_list)

@app.route("/finaltestseries", methods=["GET",'POST'])
@login_required
def finaltestseries():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    return render_template("finaltestseries.html",num=num, student_name_list=student_name_list)

###Displayed after entry to teacher
@app.route("/displaytestresults",methods=["post", "GET"])
@login_required
def displaytestresults():
    return render_template("displaytestseries.html")
@app.route("/displayfalltest",methods=["post", "GET"])
@login_required
def displayfalltest():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    global fallmarksdic
    global fallmarks
    fallmarksdic={}
    fallmarks = []
    fallmarksint=[]
    f=open("displayfalltest.txt","w+")
    for i in range(0,num):
        fallmarks.append(request.form["fallmarks{}".format(i)]+"\n")
       # fallmarks[student_list[i]]=request.form["fallmarks{}".format(i)]
    fallmarksint=[int(marks.strip('\n')) for marks in fallmarks]
    for i in range(0,num):
        fallmarksdic[student_roll_no_list[i]]=fallmarksint[i]
    f.writelines(fallmarks)
    print(fallmarksdic)
    flash(f'Marks have been saved successfully!', 'success')
    return render_template("displayfalltest.html", student_name_list=student_name_list,num=num, fallmarks=fallmarks)

@app.route("/displayspringtest", methods=["post","GET"])
@login_required
def displayspringtest():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    global springmarksdic
    global springmarks
    springmarksdic={}
    springmarks = []
    springmarksint=[]
    f = open("displayspringtest.txt", "w+")
    for i in range(0, num):
        springmarks.append(request.form["springmarks{}".format(i)] + "\n")
    springmarksint=[int(marks.strip('\n')) for marks in springmarks]
    for i in range(0,num):
        springmarksdic[student_roll_no_list[i]]=springmarksint[i]
    print(springmarksdic)
    f.writelines(springmarks)
    flash(f'Marks have been saved successfully!', 'success')
    return render_template("displayspringtest.html", student_name_list=student_name_list,num=num, springmarks=springmarks)

@app.route("/displayfinaltest", methods=["post","GET"])
@login_required
def displayfinaltest():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    global finalmarks
    global finalmarksdic
    finalmarksdic={}
    finalmarks = []
    finalmarksint=[]
    f = open("displayfinaltest.txt", "w+")

    for i in range(0, num):
        finalmarks.append(request.form["finalmarks{}".format(i)] + "\n")
    finalmarksint=[int(marks.strip('\n')) for marks in finalmarks]
    for i in range(0,num):
        finalmarksdic[student_roll_no_list[i]]=finalmarksint[i]
    print(finalmarksdic)
    f.writelines(finalmarks)
    flash(f'Marks have been saved successfully!', 'success')
    return render_template("displayfinaltest.html", student_name_list=student_name_list, num=num,finalmarks=finalmarks)

###Results Displayed to Account

@app.route("/displayfalltest1")
@login_required
def displayfalltest1():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    try:
        fallmarks[0]
    except:
        flash(f'Marks have not been uploaded yet!', 'danger')
        return redirect(url_for("home"))
    else:
        return render_template("displayfalltest1.html", student_name_list=student_name_list,num=num,fallmarks=fallmarks)

@app.route("/displayspringtest1")
@login_required
def displayspringtest1():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    try:
        springmarks[0]
    except:
        flash(f'Marks have not been uploaded yet!', 'danger')
        return redirect(url_for("home"))
    else:
        return render_template("displayspringtest1.html", student_name_list=student_name_list,num=num,springmarks=springmarks)


@app.route("/displayfinaltest1")
@login_required
def displayfinaltest1():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    try:
        finalmarks[0]
    except:
        flash(f'Marks have not been uploaded yet!', 'danger')
        return redirect(url_for("home"))
    else:
        return render_template("displayfinaltest1.html", student_name_list=student_name_list, finalmarks=finalmarks,num=num)




###Attendance

@app.route("/takeattendance",methods = ['GET', 'POST'])
def takeattendance():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    return render_template("takeattendance.html",student_name_list=student_name_list,num=num)

@app.route("/displayattendance", methods=["post", "GET"])
@login_required
def displayattendance():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    global attendance
    attendancedic = {}
    attendance = []
    f = open("attendance.txt", "w+")
    for i in range(0, num):
        try:
            request.form["att{}".format(i)]
        except:
            attendance.append("absent" + "\n")
        else:
            attendance.append(request.form["att{}".format(i)] + "\n")
    for i in range(0, num):
        attendancedic[student_roll_no_list[i]] = attendance[i]
    f.writelines(attendance)
    flash(f'Attendance has been saved successfully!', 'success')
    return render_template("displayattendance.html", student_name_list=student_name_list, attendance=attendance,num=num)

@app.route("/displayattendance1",methods=["get",'post'])
def displayattendance1():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    try:
        attendance[0]
    except:
        flash(f'Attendance has not been uploaded yet!', 'danger')
        return redirect(url_for("account"))
    return render_template("displayattendance1.html", student_name_list=student_name_list, attendance=attendance,num=num)

###enrollment
@app.route("/enrolledstudents",methods=['get','post'])
def enrolledstudents():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    return render_template("enrolledstudents.html",student_name_list=student_name_list,num=num)

@app.route("/enrolledstudentsT", methods=['get', 'post'])
def enrolledstudentsT():
    l = Student.query.all()

    student_name_list = []
    student_roll_no_list = []
    for i in l:
        i = str(i)
        a = i.split(',')
        name = a[0]
        student_name_list.append(name)
        roll_no = a[1]
        student_roll_no_list.append(roll_no)
    num=len(student_name_list)
    return render_template("enrolledstudentsT.html", student_name_list=student_name_list, num=num)





if __name__ == '__main__':
    app.run(debug=True)