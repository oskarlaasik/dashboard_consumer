import datetime
import time

import pandas as pd

from src import cache, db
from src import scheduler
from src.external_calls import get_records, get_token, post_statistics
from src.models import Answer
from src.statistics import calculate_statistics


@scheduler.task('interval', id='get_answers', seconds=1, max_instances=1)
def get_records_scheduled():
    while not cache.get('continuation_token'):
        continuation_token = get_token()
        # returns None if schema validation fails
        cache.set('continuation_token', continuation_token)
        # Answers api sends an empty array when call
        # is made immediately after asking token
        time.sleep(1)
    # returns None for either if schema validation fails
    records, token = get_records(cache.get('continuation_token'))
    cache.set('continuation_token', token)
    if records:
        answers = []
        for answer in records:
            answers.append(Answer.create(**answer))
        with scheduler.app.app_context():
            db.session.bulk_save_objects(answers)
            db.session.commit()


# Execute this task every 10 seconds
@scheduler.task('interval', id='post_statistics', seconds=10, max_instances=1)
def post_statistics_scheduled():
    now = datetime.datetime.now()
    limit = now - datetime.timedelta(minutes=1)
    with scheduler.app.app_context():
        query = Answer.query.filter(Answer.created > limit)
        df = pd.read_sql(query.statement, db.session.bind)
        num_users, num_answers, avg_correctness, correctness_stddev = calculate_statistics(df)
        post_statistics(num_users, num_answers, avg_correctness, correctness_stddev)
        Answer.delete_older_than_one_minute(now)
