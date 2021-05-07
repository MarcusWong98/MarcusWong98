# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
GET '/questions'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Fetches a string of current category
- Fetches a list of question dictionaries with question information, such as answer and category type
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
- Returns: A string that is a representation of the current category
- Returns: A list of questions that contains dictionaries for questions with several key-value pairs for different information. 5 kinds of information are contained in dictionaries. The difficulty is represented by integers. Category type is also represented by integers corresponding to different types. 
"questions": [
    {
        "answer": "test",
        "category": 2,
        "difficulty": 1,
        "id": 3,
        "question": "test"
    },
    {
        "answer": "art",
        "category": 3,
        "difficulty": 1,
        "id": 4,
        "question": "art"
    }
],

GET '/categories/<int:id>/questions' 
- Fetches a integer representation of current category type
- Fetches a list of questions with 5 kinds of information which are answer, category, difficulty, question id and question itself
- Fetches a number of how many question there are of type of the category represented by the integer
- Request Arguments: None
Returns: a list of questions with 5 kinds of information which are answer, category, difficulty, question id and question itself
[
    {
      "answer": "test",
      "category": 2,
      "difficulty": 1,
      "id": 3,
      "question": "test"
    }
]

POST '/questions'
- Send a json object to create a question
JSON.stringify({
    question: [String],
    answer: [String],
    difficulty: [Integer],
    category: [Integer]
})
Return: a json object that contains success status, true if successfully create a question
{'success': True}

       
POST '/questions/search'
- Send a json object for searching questions
JSON.stringify({searchTerm: searchTerm})
Return: a json object that contains success status, true if successfully get questions with search term. Current category type number representation corresponding to different type, a list of questions and number of total questions 
{
    "currentCategory":1,
    "questions":[{"answer":"test","category":2,"difficulty":1,"id":3,"question":"test"}],
    "success":true,
    "totalQuestions":1
}


POST '/quizzes'
- Send a json object to get new unanswered questions for quiz by quiz_category.id, and filter out unanswered questions with previous_questions
JSON.stringify({
    previous_questions: [Array],
    quiz_category: [Object]
})
Return: a json object that contains a list of questions
{
"question":{
    "answer":"art",
    "category":3,
    "difficulty":1,
    "id":4,
    "question":"art"
}}

DELETE '/questions/<int:id>'
- Delete a question with ID(Must be an integer) passed into the URI
Return: a json object that contains success status, true if successfully delete a question
jsonify({'success': True})
```

```
Error Type:

Not_found error
- If the expected value not found in db, it would return a 404 error type
{
    'success': False,
    'message': 'Not Found',
    'error': 404
}

Unprocessable error
- If something wrong in the request like making a post request without sending json, it would return a 422 error type
{
    'success': False,
    'message': 'Unprocessable',
    'error': 422
}
  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
              'success': False,
              'message': 'Unprocessable',
              'error': 422
        }), 422



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```