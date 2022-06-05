import datetime

from src import db
from src.models import Answer


def test_create_answer(app):
    with app.app_context():
        answer = Answer.create(id=10, client_timestamp='ISO 8601', user_uuid='1234-5678-9012345', correctness=1)
        db.session.add(answer)
        db.session.commit()
        assert db.session.query(Answer).one()


def test_delete_old_answers(app):
    with app.app_context():
        now = datetime.datetime.now()
        for i in range(100, 0, -1):
            answer = Answer(foreign_id=100 - i,
                            client_timestamp='ISO 8601',
                            user_uuid='1234-5678-9012345',
                            correctness=1,
                            now=now - datetime.timedelta(seconds=i)
                            )
            db.session.add(answer)
            db.session.commit()
        assert len(Answer.query.all()) == 100
        Answer.delete_older_than_one_minute(now)
        assert len(Answer.query.all()) == 60
