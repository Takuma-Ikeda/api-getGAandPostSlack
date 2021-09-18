from ga import GA
import json


# AWS Lambda ハンドラー
def lambda_handler(event, context):
    ga = GA()
    metrics = ga.exe()
    return {
        'statusCode': 200,
        'body': json.dumps(metrics)
    }


if __name__ == "__main__":
    ga = GA()
    metrics = ga.exe()
