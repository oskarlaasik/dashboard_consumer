def calculate_statistics(df):
    num_users = df.user_uuid.unique().size
    num_answers = df.shape[0]
    avg_correctness = df.correctness.mean()
    correctness_stddev = df.correctness.std()
    return num_users, num_answers, avg_correctness, correctness_stddev
