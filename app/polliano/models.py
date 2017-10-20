from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
import json
from app.models import User
class OptionList():
    pass

class Poll(db.Model):

    __tablename__ = 'polls'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    question = db.Column(db.Text, nullable=False)
    poll_image = db.Column(db.String, default="")
    options = db.Column(db.String, nullable=False)
    features = db.Column(db.String, nullable=True)
    stats = db.Column(db.String, nullable=True)
    votes = relationship("Vote", back_populates="poll")

    def __init__(self, question, options, created_by):
        self.question = question
        self.options = options
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return Poll.query.filter_by(created_by=user_id)

    @staticmethod
    def get_by_id(poll_id):
        return Poll.query.filter_by(id=poll_id)[0]

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Poll: {}>".format(self.question)

class Vote(db.Model):

    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'))
    poll = relationship("Poll", back_populates="votes")

    value = db.Column(db.String, nullable=False)

    def __init__(self, poll_id, value, created_by):
        self.poll_id = poll_id
        self.value = value
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(poll_id):
        return Vote.query.filter_by(poll_id=poll_id)

    @staticmethod
    def get_by_id(vote_id):
        return Vote.query.filter_by(id=vote_id)[0]

    @staticmethod
    def get_value_deserialized(vote_id):
        vote = Vote.query.filter_by(id=vote_id)[0]
        return json.loads(vote.value)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Vote: {}>".format(self.value)
