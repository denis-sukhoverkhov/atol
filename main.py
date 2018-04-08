from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    return app


app = create_app()
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
