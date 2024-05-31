from flask import Flask, request, jsonify, make_response
from datetime import datetime as dt
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google_utils
import os

app = Flask(__name__)
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/calendar.readonly']

@app.route("/health", methods=['GET'])
def health():
    return jsonify(success=True)

@app.route("/insert_in_document", methods=['GET'])
def insert_in_document():
    document_id = request.args.get("document_id")
    insert_payload = request.args.get("insert_payload")
    try:
        with build('docs', 'v1', credentials = google_utils.get_google_creds()) as service:
            documents = service.documents()

            body = {
                "requests":
                [
                    {"insertText":
                        {"text":insert_payload + ", ", "location":{"index":1}}
                    }
                ]
            }

            documents.batchUpdate(documentId = document_id, body = body).execute()
    except HttpError as err:
        print(err)
        raise(err)
    return jsonify(success=True)

@app.route("/clear_document_content", methods=['GET'])
def clear_document_content():
    document_id = request.args.get("document_id")
    document_content = google_utils.get_document_content(document_id)
    try:
        with build('docs', 'v1', credentials = google_utils.get_google_creds()) as service:
            documents = service.documents()

            body = {
                "requests":
                [
                    {"deleteContentRange": 
                        {"range": 
                            {
                                "startIndex": 1,
                                "endIndex": len(document_content)
                            }
                        }
                    }
                ]
            }

            documents.batchUpdate(documentId = document_id, body = body).execute()
    except HttpError as err:
        print(err)
        raise(err)
    return jsonify(success=True)

@app.route("/get_document_content", methods=['GET'])
def get_document_content():
    document_id = request.args.get("document_id")
    document_content = google_utils.get_document_content(document_id)
    response = make_response(document_content, 200)
    response.mimetype = "text/plain"
    return response

@app.route("/get_calendar_items", methods=['GET'])
def get_calendar_items():
    calendar_names = request.args.get("calendar_names")
    items_to_ignore = request.args.get("items_to_ignore")
    timeformat = request.args.get("timeformat")
    timezone = request.args.get("timezone")
    calendar_ids = []

    try:

        with build('calendar', 'v3', credentials = google_utils.get_google_creds()) as service:
            now = dt.now().isoformat()+'Z'          

            page_token = None
            while True:
                calendar_list = service.calendarList().list(pageToken=page_token).execute()
                for calendar_list_entry in calendar_list['items']:
                    if calendar_list_entry['summary'] in calendar_names:
                        calendar_ids.append(calendar_list_entry['id'])
                page_token = calendar_list.get('nextPageToken')
                if not page_token:
                    break

            for id in calendar_ids:
                events_list = service.events().list(calendarId=id, 
                                               timeMin=now,
                                               timeZone=timezone,
                                               maxResults=30,
                                               singleEvents=True,
                                               orderBy='startTime').execute()

            events = google_utils.get_calendar_events(events_list, items_to_ignore)
            calendar_items = google_utils.parse_calendar_events(events, timeformat)

    except HttpError as err:
        print(err)
        raise(err)

    return calendar_items

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['google_service_port'])
