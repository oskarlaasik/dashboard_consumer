import datetime
import time

import pandas as pd

from src import cache, db
from src.external_calls import get_records, get_token, post_statistics
from src.models import Answer
from src.statistics import calculate_statistics
from src import scheduler


@scheduler.task('interval', id='get_answers', seconds=1, max_instances=1)
def get_records_scheduled():
    continuation_token = cache.get('continuation_token')
    if not continuation_token:
        continuation_token = get_token()
        cache.set('continuation_token', continuation_token)
        # Answers api seems to send and empty array call
        # is made less than 1 second after asking for token
        time.sleep(1)
    records = get_records(continuation_token)
    cache.set('continuation_token', records['token'])
    answers = []
    for answer in records['answers']:
        answers.append(Answer.create(**answer))
    with scheduler.app.app_context():
        db.session.bulk_save_objects(answers)
        db.session.commit()


# Execute this task every 10 seconds
@scheduler.task('interval', id='post_statistics', seconds=10, max_instances=1)
def post_statistics_scheduled():
    minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)
    with scheduler.app.app_context():
        query = Answer.query.filter(Answer.created > minute_ago)
        df = pd.read_sql(query.statement, db.session.bind)
        num_users, num_answers, avg_correctness, correctness_stddev = calculate_statistics(df)
        response = post_statistics(num_users, num_answers, avg_correctness, correctness_stddev)
    print(response)
