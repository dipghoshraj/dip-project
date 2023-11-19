

from model import db

class Phone_number(db.Model):
    id = db.Column(db.Integer, nullable=False, unique=True,)
    number = db.Column(db.String(40), primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))