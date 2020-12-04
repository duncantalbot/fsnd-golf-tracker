from app import db
import json

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    handicap = db.Column(db.String())

    def __init__(self, firstname, lastname, handicap):
        self.firstname = firstname
        self.lastname = lastname
        self.handicap = handicap

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'handicap': self.handicap,
        }


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(), nullable=False)
    date = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, event_type, date, description):
        self.event_type = event_type
        self.date = date
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'event_type': self.event_type,
            'date': self.date,
            'description': self.description
        }
