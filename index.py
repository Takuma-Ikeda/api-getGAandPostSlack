from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import requests, json, datetime

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'key_file.json'
VIEW_ID = ''
SLACK_WEB_HOOK_URL = ''

'''
Google アナリティクス Reporting API v4 リファレンス
https://developers.google.com/analytics/devguides/reporting/core/v4/basics

メトリクス指定方法
https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/
'''


def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    # 過去 7 日間のデータ取得
                    # 'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                    # 昨日のデータ取得
                    'dateRanges': [{'startDate': 'yesterday', 'endDate': 'yesterday'}],
                    # 欲しいデータの種類
                    'metrics': [
                        {"expression": "ga:users"},      # Users
                        {'expression': 'ga:sessions'},   # Sessions
                        {"expression": "ga:pageviews"}   # PV
                    ],
                    # 国ごとに分けたい場合
                    # 'dimensions': [{'name': 'ga:country'}]
                }]
        }
    ).execute()


def get_metrics(response):
    metrics = {}
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ' + dimension)

            for i, values in enumerate(dateRangeValues):
                # print('Date range: ' + str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    print(metricHeader.get('name') + ': ' + value)
                    metrics[metricHeader.get('name')] = value
    return metrics


def post_slack(metrics):
    users = metrics['ga:users']
    sessions = metrics['ga:sessions']
    pvs = metrics['ga:pageviews']
    dt_yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    str_yesterday = dt_yesterday.strftime('%Y年%m月%d日')

    requests.post(SLACK_WEB_HOOK_URL, json.dumps({
        'text': str_yesterday + '\n[USERS] ' + users + '\n[SESSIONS] ' + sessions + '\n[PVS] ' + pvs,
        'username': 'GA-Bot',
        'icon_emoji': ':chart_with_upwards_trend:',
        'link_names': 1,
    }))


# AWS Lambda ハンドラー
def lambda_handler(event, context):
    metrics = exe()
    return {
        'statusCode': 200,
        'body': json.dumps(metrics)
    }


def exe():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    metrics = get_metrics(response)
    post_slack(metrics)
    return metrics


if __name__ == "__main__":
    exe()
