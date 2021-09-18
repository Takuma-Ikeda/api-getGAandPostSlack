from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import datetime
import json
import os
import requests

'''
Google アナリティクス Reporting API v4 リファレンス
https://developers.google.com/analytics/devguides/reporting/core/v4/basics

メトリクス指定方法
https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/
'''


class GA:

    def __init__(self):
        load_dotenv()

        self.SCOPES = [os.getenv('SCOPE')]
        self.KEY_FILE_LOCATION = os.getenv('KEY_FILE_LOCATION')
        self.VIEW_ID = os.getenv('VIEW_ID')
        self.SLACK_WEB_HOOK_URL = os.getenv('SLACK_WEB_HOOK_URL')

    def exe(self):
        analytics = self.__initialize_analytics_reporting()
        response = self.__get_report(analytics)
        metrics = self.__get_metrics(response)
        self.__post_slack(metrics)

        return metrics

    def __initialize_analytics_reporting(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.KEY_FILE_LOCATION, self.SCOPES)
        analytics = build('analyticsreporting', 'v4', credentials=credentials)

        return analytics

    def __get_report(self, analytics):
        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': self.VIEW_ID,
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

    def __get_metrics(self, response):
        metrics = {}
        for report in response.get('reports', []):
            column_header = report.get('columnHeader', {})
            dimension_headers = column_header.get('dimensions', [])
            metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

            for row in report.get('data', {}).get('rows', []):
                dimensions = row.get('dimensions', [])
                date_range_values = row.get('metrics', [])

                for header, dimension in zip(dimension_headers, dimensions):
                    print(header + ': ' + dimension)

                for i, values in enumerate(date_range_values):
                    # print('Date range: ' + str(i))
                    for metric_header, value in zip(metric_headers, values.get('values')):
                        print(metric_header.get('name') + ': ' + value)
                        metrics[metric_header.get('name')] = value

        return metrics

    def __post_slack(self, metrics):
        users = metrics['ga:users']
        sessions = metrics['ga:sessions']
        pvs = metrics['ga:pageviews']
        dt_yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        str_yesterday = dt_yesterday.strftime('%Y年%m月%d日')

        requests.post(self.SLACK_WEB_HOOK_URL, json.dumps({
            'text': str_yesterday + '\n[USERS] ' + users + '\n[SESSIONS] ' + sessions + '\n[PVS] ' + pvs,
            'username': 'GA-Bot',
            'icon_emoji': ':chart_with_upwards_trend:',
            'link_names': 1,
        }))
