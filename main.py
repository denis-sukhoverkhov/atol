import contextlib
import io
import sqlite3

from flask import g, Flask
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def create_app(debug=False) -> Flask:
    app = Flask(__name__)
    app.debug = debug
    return app


app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('age')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    register_date = db.Column(db.DateTime, default=db.func.now())
    last_activity = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"User {self.name}"


user_fields = {
    'name': fields.String,
    'age': fields.Integer,
    'register_date': fields.DateTime(dt_format='rfc822'),
    'last_activity': fields.DateTime(dt_format='rfc822'),
}


class UserApi(Resource):

    @marshal_with(user_fields)
    def get(self):
        return User.query.all()

    @marshal_with(user_fields)
    def post(self):
        args = parser.parse_args()
        user = User(name=args.name, age=args.age)
        db.session.add(user)
        db.session.commit()
        return user, 201

    # def put(self, todo_id):
    #     todos[todo_id] = request.form['data']
    #     return {todo_id: todos[todo_id]}


api.add_resource(UserApi, '/user')


zen = io.StringIO()
with contextlib.redirect_stdout(zen):
    pass


@app.route('/')
def index():
    return zen.getvalue().replace('\n', '</br>')


if __name__ == '__main__':
    db.create_all()
    app.run()
