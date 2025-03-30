from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db=SQLAlchemy()


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    fullname=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    dob=db.Column(db.Date,nullable=False)


class subjects(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     subject_name=db.Column(db.String(100),nullable=False)
     discription=db.Column(db.Text,nullable=False)
     chapters=db.relationship('chapters',backref='author',lazy=True,cascade="all, delete")

class chapters(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     chapter_name=db.Column(db.String(100),nullable=False)
     discription=db.Column(db.Text,nullable=False)
     questions=db.relationship('questions',backref='author',lazy=True,cascade="all, delete")
     subject_id=  db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)

class questions(db.Model):
      id=db.Column(db.Integer,primary_key=True)
      title=db.Column(db.String(100),nullable=False)
      statement=db.Column(db.Text,nullable=False)
      option1=db.Column(db.Integer,nullable=False)
      option2=db.Column(db.Integer,nullable=False)
      option3=db.Column(db.Integer,nullable=False)
      option4=db.Column(db.Integer,nullable=False)
      correct_option=db.Column(db.Integer,nullable=False)
      chapter_id=db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
