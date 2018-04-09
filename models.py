
from main import db, app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    register_date = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime)

    def __repr__(self):
        return f"User {self.username}"


if __name__ == '__main__':
    db.create_all()
