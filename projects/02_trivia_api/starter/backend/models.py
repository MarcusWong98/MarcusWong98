import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "trivia"
database_path = "postgres://{}:{}@{}/{}".format('postgres', '19980906aB','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question

'''
# question_category = db.Table(
#     'question_category', 
#     db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True), 
#     db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
# )

class Question(db.Model):  
  __tablename__ = 'questions'

  id = db.Column(db.Integer, primary_key=True)
  question = db.Column(db.String())
  answer = db.Column(db.String())
  category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
  difficulty = db.Column(db.Integer)


  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String())


  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }


class Function():
      
  QUESTIONS_PER_PAGE = 10
  
  def formatting(self, collections, start, end):
    formatted_collections = []
    
    if start is not Integer or end is not Integer:
      formatted_collections = [collection.format() for collection in collections]
    else: 
      formatted_collections = [collection.format() for collection in collections[start:end]]

    return formatted_collections
  
  def pagination(self, page, collections):
        
    start = (page - 1) * self.QUESTIONS_PER_PAGE

    if start > len(collections): return None

    end = start + self.QUESTIONS_PER_PAGE

    formatted_collections = self.formatting(collections=collections, start=start, end=end)

    return formatted_collections


