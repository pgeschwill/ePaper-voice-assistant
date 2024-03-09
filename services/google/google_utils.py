from datetime import datetime as dt
from dateutil.parser import parse as dtparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/calendar.readonly']
PATH_TO_THIS_FILE = os.path.dirname(os.path.abspath(__file__))

def get_google_creds():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    path_to_token = os.path.join(PATH_TO_THIS_FILE, "auth", "token.json")
    path_to_client_secret = os.path.join(PATH_TO_THIS_FILE, "auth", "client_secret.json")
    if os.path.exists(path_to_token):
        creds = Credentials.from_authorized_user_file(path_to_token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path_to_client_secret, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path_to_token, 'w') as token:
            token.write(creds.to_json())

    return creds

def get_document_content(document_id):
    try:
        with build('docs', 'v1', credentials = get_google_creds()) as service:
            documents = service.documents()
            document = documents.get(documentId = document_id).execute()
    except HttpError as err:
        print(err)
        raise(err)
    
    return document["body"]["content"][1]["paragraph"]["elements"][0]["textRun"]["content"]

def get_calendar_events(events_list, items_to_ignore):
    events = {}
    for event in events_list.get('items', []):
        if event['summary'] in items_to_ignore:
            continue
        initial_start = event['start'].get('dateTime', event['start'].get('date'))
        start = "%s-0" % initial_start
        counter = 0
        while start in list(events.keys()):
            counter += 1
            start = "%s-%s" % (initial_start, counter)

        events[start] = event

    return events

def parse_calendar_events(events, timeformat):
    calendar_items = []

    for event_key in sorted(events.keys()):
        start = events[event_key]['start'].get('dateTime', events[event_key]['start'].get('date'))
        end = events[event_key]['end'].get('dateTime', events[event_key]['end'].get('date'))

        if timeformat == "12h":
            start_date = dt.strftime(dtparse(start), '%m-%d')
            start_time = dt.strftime(dtparse(start), '%I:%M %p')
            end_date = dt.strftime(dtparse(end), '%m-%d')
            end_time = dt.strftime(dtparse(end), '%I:%M %p')
        else:
            start_date = dt.strftime(dtparse(start), '%d.%m.')
            start_time = dt.strftime(dtparse(start), '%H:%M')
            end_date = dt.strftime(dtparse(end), '%d.%m.')
            end_time = dt.strftime(dtparse(end), '%H:%M')

        week = dt.strftime(dtparse(start), '%W')

        calendar_items.append({
            "start_date": start_date,
            "end_date": end_date,
            "start_time": start_time,
            "end_time": end_time,
            "content": events[event_key]['summary'],
            "week": int(week)
        })
        
    return calendar_items