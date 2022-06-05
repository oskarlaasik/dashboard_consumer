import datetime

from src import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foreign_id = db.Column(db.Integer)
    client_timestamp = db.Column(db.String(256))
    user_uuid = db.Column(db.String(256))
    correctness = db.Column(db.Float)
    created = db.Column(db.DateTime)

    def __init__(self, foreign_id, client_timestamp, user_uuid, correctness, now):
        self.foreign_id = foreign_id
        self.client_timestamp = client_timestamp
        self.user_uuid = user_uuid
        self.correctness = correctness
        self.created = now

    # Not a static function because we always insert in bulk
    def create(id, client_timestamp, user_uuid, correctness):  # create new Answer
        new_answer = Answer(id, client_timestamp, user_uuid, correctness, datetime.datetime.now())
        return new_answer

    @staticmethod
    def delete_older_than_one_minute(now):  # include now for testing
        limit = now - datetime.timedelta(minutes=1)
        Answer.query.filter(limit > Answer.created).delete()
        db.session.commit()

