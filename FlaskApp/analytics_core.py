import argparse
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
import pprint
from oauth2client import client
from oauth2client import file
from oauth2client import tools

pp = pprint.PrettyPrinter(indent=10)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = '/var/www/FlaskApp/FlaskApp/a.p12'
SERVICE_ACCOUNT_EMAIL = 'testing@macro-creek-152218.iam.gserviceaccount.com'
VIEW_ID = '135470943'


def initialize_analyticsreporting():

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

  return analytics


def get_report(analytics, campaign=None, source=None, startDate='7daysAgo', endDate='today'):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  
  if campaign:
    return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{"name": "ga:campaign"}],
          "dimensionFilterClauses": [
                                      {
                                        "filters": [
                                          {
                                            "dimensionName": "ga:campaign",
                                            "operator": "EXACT",
                                            "expressions": [campaign]
                                          }
                                        ]
                                      }
                                    ]
        }]
      }
    ).execute()

  elif source:
    return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{"name": "ga:source"}],
          "dimensionFilterClauses": [
                                      {
                                        "filters": [
                                          {
                                            "dimensionName": "ga:source",
                                            "operator": "EXACT",
                                            "expressions": [source]
                                          }
                                        ]
                                      }
                                    ]
        }]
      }
    ).execute()

  else:
    return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{"name": "ga:source"}]
        }]
      }
    ).execute()

def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response"""

  print response

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print header + ': ' + dimension

      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print value 
          return value