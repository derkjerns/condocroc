from app import db
from sqlalchemy.dialects.postgresql import JSON


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    url = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.String())

    def __init__(self, title, url, description, date):
        self.title = title
        self.url = url
        self.description = description
        self.date = date

    def __repr__(self):
        return '<id {}>'.format(self.id)
