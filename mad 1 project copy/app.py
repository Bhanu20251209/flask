from flask import Flask,render_template,redirect,request,flash,url_for
from model import *
from flask_login import login_user, logout_user, login_required, current_user,LoginManager

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'your_secret_key_here' 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///householdservice.sqlite3'

db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'login'  
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
prof=[]
n=None
@app.route('/')
def home():
    return redirect(url_for('login'))
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='GET':
        return render_template('login.html',servicer="servicer__details",customer='customer_details')
    elif request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email,password=password).first()
        if user :
            login_user(user)
            return redirect(url_for('customer_dashbord'))
        elif email=="admin@gmail.com" and   password=="admin123":
            return redirect(url_for('Admin'))
        else:
            flash('Invalid email or password','danger')
            return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/customer/signup',methods=['POST','GET'])
def customer_details():
    if request.method=='GET':
        return render_template('customer-signup.html',login='login')
    elif request.method=='POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']  
        address = request.form['address']
        pincode = request.form['pincode']
        p=request.form['phone']
        c=customer( name=name, email=email,password=password,phone=p,address=address,pincode=pincode  )
        u=User( name=name,email=email,password=password,roll="customer")
        db.session.add(c)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('login'))

    else:
        return "<h1>404</h1>"
@app.route('/customer/Dashbord',methods=['GET'])
@login_required
def customer_dashbord():
    c=catogery.query.all()
    return  render_template('customer-home.html',login='login',s=c,name=current_user.name,book='book')
@app.route('/customer/Dashbord/<int:id>',methods=['GET'])
def book(id):
   s=services.query.filter_by(catogery_id=id).all()
   return render_template('customer-book.html',login='logout',s=s,name=current_user.name,b='service_booking') 

@app.route('/customer/Dashbord/book/<int:bid>', methods=['GET'])
def service_booking(bid):
       s=services.query.filter_by(id=bid).all()
       c=customer.query.filter_by(name=current_user.name).all()
       b=bookings(customer_id=c[0].id,sercices_id=s[0].id,status=False)
       db.session.add(b)
       db.session.commit()
       return redirect(url_for('book',id=s[0].catogery_id))
@app.route('/customer/Dashbord/<string:name>/search',methods=['GET','POST'])
def customer_search(name):
    if request.method=='GET':
        typ=request.form['search_by']

     



@app.route('/Service_Professional/signup',methods=['POST','GET'])
def servicer__details():
    if request.method=='GET':
        s=services.query.all()
        return render_template('professional-signup.html',login='logout',services=s)
    elif request.method=='POST':
        file=request.files['file']
        l={'fullname' : request.form['fullname'],'email':request.form['email'],'phone':request.form['phone'],'password':request.form['password'], 'experience':request.form['exp'],'service':request.form['services'],'address':request.form['address'],'pincode':request.form['pincode'],'filename':file.filename,'data':file.read()}
        prof.append(l)
        return "seccses"
    else:
        return "error"
@app.route('/Service_Professional/Dashbord',methods=['POST','GET'])
def service_professional_dashbord():
    b=
@app.route('/Approve/<int:id>', methods=['GET'])
def approve_info(id):
        d=prof[id]
        s=servicer(fullname=d['fullname'], email=d['email'],phone=d['phone'],password=d['password'],experience=d['experience'],service=d['service'],address=d['address'],pincode=d['pincode'],filename=d['filename'],data=d['data'])
        u=User(name=d['fullname'],email=d['email'],password=d['password'],roll="servicer")
        db.session.add(s)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('Admin'))
@app.route('/admin',methods=['POST','GET'])
@login_required
def Admin():
        c=services.query.all()
        return render_template('admin_dashbord.html',login='login',admin='Admin',service=c,new='newservice',delete='delete_info',edit='edit_info',prof=prof,approve='approve_info')
@app.route('/delete/<int:service_id>', methods=['GET'])
def delete_info(service_id):
        u=services.query.get_or_404(service_id)
        db.session.delete(u)
        db.session.commit()
        return redirect(url_for('Admin'))
@app.route('/admin/service',methods=['POST','GET'])
def newservice():
    if request.method=='GET':
        return render_template('services.html')
    elif request.method=='POST':
        name=request.form['catogery']
        c=catogery.query.filter_by(name=name).first()
        print(c)
        if not c:
           c=catogery(name=name)
           db.session.add(c)
           db.session.commit()

        s=services(name=request.form['serviceName'],catogery_id=c.id,discription=request.form['discription'],price=request.form['price'])
        
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('Admin'))
    else:
        return "error"
if __name__=='__main__':
    app.run(debug=True,port=5500,host='0.0.0.0')