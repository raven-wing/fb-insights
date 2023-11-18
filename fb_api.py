import requests
import datetime

GRAPH_API_VERSION = "v18.0"


class DateRange:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date


def date_to_timestamp(date: str):
    return int(datetime.datetime.strptime(date, '%Y-%m-%d').timestamp())


def get_facebook_page_insights(page_id, access_token, metrics=None, date_range=DateRange('2023-01-01', '2023-01-31')):
    """ Gets Facebook Page Insights for the specified metrics and date range.
    :param page_id: Facebook Page ID
    :param access_token: Facebook Page Access Token
    :param metrics: List of metrics to retrieve
    :param date_range: Date range to retrieve data for
    :return: JSON response from Facebook API"""

    metrics = metrics or ['page_impressions', 'page_engaged_users']

    api_endpoint = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/insights"
    params = {
        'access_token': access_token,
        'metric': ','.join(metrics),
        'period': 'day',
        'since': date_range.start_date,
        'until': date_range.end_date
    }

    response = requests.get(api_endpoint, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(f"Error: {response.text}")
        return None


def parse_insights(insights):
    result = {}
    for insight in insights['data']:
        values = insight['values']
        metric_name = insight['name']
        result[metric_name] = {}
        for value in values:
            metric_date = value['end_time'][:10]
            metric_value = value['value']
            result[metric_name].update({metric_date: metric_value})
    return result
