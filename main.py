import sqlite3

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    return app


app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    cur = get_db().cursor()
    return 'rrr'


if __name__ == '__main__':
    app.run()
