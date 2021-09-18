from dotenv import load_dotenv
import datetime
import json
import os
import requests


class Slack:

    def __init__(self, metrics):
        load_dotenv()
        self.slack_web_hook_url = os.getenv('SLACK_WEB_HOOK_URL')
        self.users = metrics['ga:users']
        self.sessions = metrics['ga:sessions']
        self.pvs = metrics['ga:pageviews']
        self.bot_name = 'GA-Bot'
        self.bot_emoji = ':chart_with_upwards_trend:'

    def post(self):
        requests.post(self.slack_web_hook_url, json.dumps({
            'text': self.__create_text(),
            'username': self.bot_name,
            'icon_emoji': self.bot_emoji,
            # ポストされるメンションの有効化
            'link_names': 1,
        }))

    def __create_text(self):
        dt_yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

        return dt_yesterday.strftime('%Y年%m月%d日')\
            + '\n[USERS] ' + self.users\
            + '\n[SESSIONS] ' + self.sessions\
            + '\n[PVS] ' + self.pvs
