from app import db


class Account(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    calls = db.relationship('Phone_number', backref='user', lazy=True)

