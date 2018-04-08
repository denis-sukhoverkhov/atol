import sqlite3

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def create_app(debug=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE}"
    app.debug = debug
    return app


app = create_app()
db = SQLAlchemy(app)


@app.route('/')
def index():
    cur = get_db().cursor()


if __name__ == '__main__':
    app.run()
