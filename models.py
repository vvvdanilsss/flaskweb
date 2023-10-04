from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    message = db.Column(db.String(120))

    def __repr__(self):
        return f'<User {self.username}>'
