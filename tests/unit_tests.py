import math

import pandas as pd

from src import db
from src.models import Answer
from src.statistics import calculate_statistics


def test_calculate_statistics(app):
    correctness = [1, 0.5, 1, 0.5]
    with app.app_context():
        answers = [
            Answer.create(id=10, client_timestamp='ISO 8601', user_uuid='1234-5678-9012345',
                          correctness=correctness[0]),
            Answer.create(id=20, client_timestamp='ISO 8601', user_uuid='1234-5678-9012345',
                          correctness=correctness[1]),
            Answer.create(id=30, client_timestamp='ISO 8601', user_uuid='1234-5678-9012345',
                          correctness=correctness[2]),
            Answer.create(id=40, client_timestamp='ISO 8601', user_uuid='1234-5678-9012346',
                          correctness=correctness[3])
        ]
        db.session.bulk_save_objects(answers)
        db.session.commit()
        query = Answer.query
        df = pd.read_sql(query.statement, db.session.bind)
    num_users, num_answers, avg_correctness, correctness_stddev = calculate_statistics(df)
    assert num_users == 2
    assert num_answers == 4
    assert avg_correctness == 0.75
    assert correctness_stddev == math.sqrt(
        sum([(c - avg_correctness) ** 2 for c in correctness]) / (len(correctness) - 1))
