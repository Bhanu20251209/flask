from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
db=SQLAlchemy()
class User(db.Model, UserMixin):
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    roll=db.Column(db.String(100),nullable=False)

    

class customer(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(100),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
             

class servicer(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    fullname=db.Column(db.String(100),nullable=False)
    service=db.Column(db.Integer,nullable=False)
    experience=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(100),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    filename=db.Column(db.String(100))
    data=db.Column(db.LargeBinary)

class catogery(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    services = db.relationship('services', backref='catogery', lazy=True)

class services(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    discription=db.Column(db.Text,nullable=False)
    catogery_id = db.Column(db.Integer, db.ForeignKey(catogery.id))
    price=db.Column(db.Integer,nullable=False)

class bookings(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(customer.id))
    sercices_id=db.Column(db.Integer,db.ForeignKey(services.id))
    status=db.Column(db.Boolean, nullable=False)
