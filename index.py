from ga import GA
from slack import Slack
import json


def exe():
    ga = GA()
    metrics = ga.get_metrics()

    slack = Slack(metrics)
    slack.post()

    return metrics


# AWS Lambda ハンドラー
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(exe())
    }


if __name__ == "__main__":
    exe()
