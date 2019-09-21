from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, number_range

"""class EnrollmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Enter Email', validators=[DataRequired(),Email(), Length(min=5, max=30)])
    roll_no = IntegerField('Assign Roll Number', validators=[DataRequired()])
    password = PasswordField('Assign Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Enroll')"""

class MakeAnnouncementForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(),Length(min=5, max=200)])
    content = TextAreaField("Enter Content",validators=[DataRequired(),Length(min=10,max=2000)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    roll_no = IntegerField('Roll Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    admin_id = StringField('Admin ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TeacherLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class StudentScheduleForm(FlaskForm):
    roll_no = IntegerField('Enter your Roll Number', validators=[DataRequired()])
    wakeuptime = IntegerField('Enter the time you usually wakeup', validators=[DataRequired(), number_range(min=0, max=2400)])
    sleeptime = IntegerField('Enter the time you usually sleep', validators=[DataRequired(), number_range(min=0, max=2400)])
    breakfasttime = IntegerField('What time do you usually have breakfast?', validators=[DataRequired(), number_range(min=0, max=2400)])
    lunchtime = IntegerField('What time do you usually have lunch?', validators=[DataRequired(), number_range(min=0, max=2400)])
    dinnertime = IntegerField('What time do you usually have dinner?', validators=[DataRequired(), number_range(min=0, max=2400)])
    schoolgoing = IntegerField('What time do you usually leave for school?', validators=[DataRequired(), number_range(min=0, max=2400)])
    schoolreturning = IntegerField('What time do you usually return from school?', validators=[DataRequired(), number_range(min=0, max=2400)])
    #academy = BooleanField('Please select if you go to academy')
    #if academy:
    academygoing = IntegerField('What time do you usually go to the academy?')
    academyreturning = IntegerField('What time do you return from the academy?')
    #conditions = BooleanField('All times are in 2400 hrs?')
    #if conditions:
     #
    falltest = IntegerField('Fall test marks', validators=[DataRequired(), number_range(min=0, max=50)])
    springtest = IntegerField('Spring test marks', validators=[DataRequired(), number_range(min=0, max=50)])
    #finaltest = IntegerField('Final test marks', validators=[DataRequired()])
    submit = SubmitField('Enter Info')

#class StudentAcademicDetailsForm(FlaskForm):
 #   falltest = IntegerField('OHT-1 marks', validators=[DataRequired(), range(0, 51)])
  #  springtest = IntegerField('Spring test marks', validators=[DataRequired(), range(0, 51)])
   # finaltest = IntegerField('Final test marks', validators=[DataRequired(), range(0, 101)])
    #submit = SubmitField('Enter marks')





