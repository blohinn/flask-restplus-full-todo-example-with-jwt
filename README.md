# Full Flask-RESTPlus TODO App Example
This is my  example for nice [Flask-RESTPlus Flask extension](http://flask-restplus.readthedocs.io/en/stable/)

Features:
-------
 - Expandable, understandable and nice project structure with namespaces and blueprints
 - Auth with JWT with refresh tokens and supporting multiple devices of the same user
 - Custom `ValidationExeption` and exeption handler for example
 - Tests for example
 - Database interaction with [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)

## Getting Started

Installing (in project folder):

    py -m venv venv
    . venv/Scripts/activate
    # In venv:
    pip install -r requirements.txt
    export CONFIG_TYPE=dev
    py manage.py db_init


Running app:

    # In venv:
    py manage.py run

 And go to: `http://127.0.0.1:5000/api/v1/`

Running tests:

    # In venv
    export CONFIG_TYPE=tests
    py manage.py run_tests

----------
I will be glad to feedback!