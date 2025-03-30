from flask import Flask,render_template,request,redirect,jsonify,url_for
from model import *
from sqlalchemy import text
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app=Flask(__name__,instance_relative_config=True)
app.config['SECRET_KEY'] = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///quizmaster.sqlit3"

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
with app.app_context():
    db.create_all()




 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register',methods=['POST','GET'])
def signup():
    if request.method =='GET':
        return render_template('register.html')
    elif request.method =='POST':
        data = request.form.to_dict()
        dob_value = data.get('date', None)
        if dob_value:
            dob = datetime.strptime(dob_value, '%Y-%m-%d').date()
        else:
            dob = None  
        if data['password'] != data['confirmpassword']:
            return error
        user= User(fullname=data['fullname'],email=data['email'],password=data['password'],dob=dob)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return "errror"
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='GET':
          return render_template('log.html')
    elif request.method=='POST':
      data = request.form.to_dict()
      email=data.get('email')
      password=data.get('password')
      user=User.query.filter_by(email=email,password=password).first()
      load_user(user.id)
      return 'ok'
    else:
        return "error"
@app.route('/admin/home',methods=['POST','GET'])
def admin():
    sub=subjects.query.all()
    chp=chapters.query.all()
    l = db.session.execute(text("SELECT subject_id FROM chapters")).fetchall() 
    l_list = [row[0] for row in l]
    return render_template('admindashboard.html',count=l_list,subject=sub,chapter=chp,add='add_subject',addc='add_chapter',home='admin',quiz='quiz',delete='delete',edit='edit')


@app.route('/admin/add_subject',methods=['POST','GET'])
def add_subject():
    if request.method=="GET":
        return render_template('newsubject.html',h='admin')
    elif request.method=="POST":
        data = request.form.to_dict()
        sub=subjects(subject_name=data['subject'],discription=data['discription'])
        db.session.add(sub)
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return 'error'

@app.route('/admin/edit/<int:id>/<string:name>',methods=['POST','GET'])
def edit(id,name):
    
    if request.method=="GET":
       if name=='subject': return render_template('newsubject.html',h='admin',oldsub=subjects.query.get(id))
       if name=='chapter': return render_template('newchapter.html',h='admin',oldchp=chapters.query.get(id))
       if name=='question': return render_template('addqustion.html',id=id,oldq=questions.query.get(id))
    elif request.method=="POST":
        data = request.form.to_dict()
        if name=='subject':
            oldsub=subjects.query.get(id)
            oldsub.subject_name=data['subject'] 
            oldsub.discription=data['discription']
        if name=='chapter':
            oldchp=chapters.query.get(id)
            oldchp.chapter_name=data['chapter'] 
            oldchp.discription=data['discription']
        if name=='question':
            oldq=questions.query.get(id)
            oldq.title=data['title']
            oldq.statement=data['statement']
            oldq.option1=data['option1']
            oldq.option2=data['option2']
            oldq.option3=data['option3']
            oldq.option4=data['option4']
            oldq.correct_option=data['correct_option']
            db.session.commit()
            return redirect(url_for('quiz'))

        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return 'error'

@app.route('/admin/add_chapter/<int:id>',methods=['POST','GET'])
def add_chapter(id):
    if request.method=="GET":
        return render_template('newchapter.html',h='admin')
    elif request.method=="POST":
        data = request.form.to_dict()
        chp=chapters(chapter_name=data['chapter'],discription=data['discription'],subject_id=id)
        db.session.add(chp)
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return 'error'
@app.route('/admin/quiz',methods=['POST','GET'])
def quiz():
    chp=chapters.query.all()
    question=questions.query.all()
    l = db.session.execute(text("SELECT chapter_id FROM questions")).fetchall() 
    l_list = [row[0] for row in l]
    return render_template('quiz.html',l=l_list,chapter=chp,question=question,home='admin',addq='add_question',delete='delete',edit='edit')

@app.route('/delete/<int:id>/<string:name>')
def delete(id, name):
   if name == 'subject':
       subj=subjects.query.get(id)
       db.session.delete(subj)
   if name == 'chapters':
       chap=chapters.query.get(id)
       db.session.delete(chap)
   if name == 'questions':
       q=questions.query.get(id)
       db.session.delete(q)
       db.session.commit()
       return redirect(url_for('quiz'))
   db.session.commit()
   return redirect(url_for('admin'))

@app.route('/admin/quiz/addquestion/<int:id>',methods=['POST','GET'])
def add_question(id):
    if request.method=='GET':
        return render_template('addqustion.html',id=id)
    elif request.method=='POST':
        data = request.form.to_dict()
        q=questions(title=data['title'],statement=data['statement'],option1=data['option1'],option2=data['option2'],option3=data['option3'],option4=data['option4'],correct_option=data['correct_option'],chapter_id=id)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('quiz'))
    else:
        return 'error'


if __name__=="__main__":
    app.run(debug=True,port=5500,host='0.0.0.0')
