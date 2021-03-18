import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
password = '19980906aB'

database_name = 'fyyur'

SQLALCHEMY_DATABASE_URI = f'postgres://postgres:{password}@localhost:5432/{database_name}'
