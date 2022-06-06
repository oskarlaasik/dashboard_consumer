import datetime
import json

import requests


def get_token():
    response = requests.get('http://test-task.lingvist.io:3000/api/subscribe')
    if response.status_code == 200:
        return json.loads(response.content)['token']
    else:
        return None


def get_records(token):
    response = requests.get(f'http://test-task.lingvist.io:3000/api/answers/{token}')
    records = None
    token = None
    if response.status_code == 200:
        content = json.loads(response.content)
        if 'answers' in content and content['answers']:
            records = content['answers']
        if 'token' in content:
            token = content['token']
    return records, token


def post_statistics(num_users, num_answers, avg_correctness, correctness_stddev):
    iso_time = datetime.datetime.now().isoformat()
    payload = {
        "timestamp": iso_time,
        "per_minute": {
            "number_of_users": num_users,
            "number_of_answers": num_answers,
            "average_correctness": avg_correctness,
            "correctness_stddev": correctness_stddev
        }
    }
    requests.post('http://test-task.lingvist.io:3000/api/dashboard', json=payload)
