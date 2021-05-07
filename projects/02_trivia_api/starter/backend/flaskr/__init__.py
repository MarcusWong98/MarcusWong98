import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


from models import setup_db, Question, Category, db, Function

QUESTIONS_PER_PAGE = 10

functions = Function()

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # CORS(app, resources = {r'*/api/*': {origins : '*'}})
  CORS(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')

        return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods = ['GET'])
  def get_categories():
        json = request.get_json()

        if json is not None:
              abort(404)
        
        categories = Category.query.all()

        categories_dict = {}

        for category in categories:
            categories_dict[category.id] = category.type

        print(categories_dict)

        return jsonify({'categories':categories_dict, 'success': True})





  '''
    url: '/questions', 
    url: `/questions?page=${this.state.page}`,
    url: `/categories`,
  '''

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods= ['GET'])
  def get_questions():
        
        if request.get_json() is not None:
            abort(422)

        questions = Question.query.all()
      
        test = Question.query.first()
        categories = Category.query.all()

        page = request.args.get('page', 1, type=int)

      #   start = (page - 1) * QUESTIONS_PER_PAGE

      #   end = start + QUESTIONS_PER_PAGE

      #   question_selections = [question.format() for question in questions[start:end]]
        question_selections = functions.pagination(page, questions)

        categories_dict = {}

        for category in categories:
            categories_dict[category.id] = category.type
      

        if question_selections is None or len(question_selections) == 0:
              abort(404)

        return jsonify({'questions': question_selections, 'success': True, 'total_questions': len(questions), 'current_category' : 'test', 'categories': categories_dict})



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods = ['DELETE'])
  def delete_question(id):
        question = Question.query.filter_by(id = id).one_or_none()

      #   print(dir(question))
        print('question:')
        print(question)

        if question is None:
            abort(404)

        print('deleting')

        db.session.delete(question)

        db.session.commit()

        return jsonify({'success': True})


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.


  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
        question_json = request.get_json()

        if question_json is None:
            abort(422)

        question = Question(question=question_json['question'], answer=question_json['answer'], category=question_json['category'], difficulty=question_json['difficulty'])

        db.session.add(question)
        db.session.commit()

        return jsonify({'success': True})
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():

        data = request.json

        search_term = data['searchTerm']

        print(search_term)
        
        if search_term is None:
              abort(422)
            
      #   print('testestset')
       
      #   print(json_obj)

        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        if len(questions) == 0:
            abort(404)

        formatted_questions = functions.formatting(collections=questions, start=None, end=None)

      #   if len(formatted_questions) == 0:
      #       print(len(formatted_questions))
      #       abort(404)
      #        questions: result.questions,
      #     totalQuestions: result.total_questions,
      #     currentCategory: result.current_category })

        return jsonify({'questions': formatted_questions, 'totalQuestions': len(formatted_questions), 'currentCategory':1, 'success': True})

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_category_questions(id):

      #   questions: result.questions,
      #     totalQuestions: result.total_questions,
      #     currentCategory: result.current_category


        category = Category.query.get(id)    
        
        if category == None:
            abort(404)

        questions = Question.query.filter_by(category = category.id).all()

        formatted_questions = functions.formatting(questions, start = None, end=None)

        return jsonify({'questions': formatted_questions, 'totalQuestions': len(formatted_questions), 'currentCategory': category.id, 'success': True})

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def get_quizess():
        json = request.get_json()

        questions = Question.query.filter(Question.category == json['quiz_category']['id']).all()

        formatted_questions = [question.format() for question in questions if question.id not in json['previous_questions']]

        print(formatted_questions)

        return jsonify({'question': formatted_questions[0]})

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
              'success': False,
              'message': 'Not Found',
              'error': 404
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
              'success': False,
              'message': 'Unprocessable',
              'error': 422
        }), 422

  return app


    