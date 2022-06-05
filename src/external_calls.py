import datetime
import json

import requests


def get_token():
    response = requests.get('http://test-task.lingvist.io:3000/api/subscribe')
    content = response.content.decode("utf-8")
    token = json.loads(content)['token']
    return token


def get_records(token):
    response = requests.get(f'http://test-task.lingvist.io:3000/api/answers/{token}')
    records = json.loads(response.content)
    return records


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
    response = requests.post('http://test-task.lingvist.io:3000/api/dashboard', json=payload)
    return response
