import requests

class GoogleServiceWrapper:

    def __init__(self, config):
        self.google_service_url = "http://google-service:6000"
        self.calendar_names = config["google"]["calendar"]["calendar_names"]
        self.items_to_ignore = config["google"]["calendar"]["items_to_ignore"]
        self.timeformat = config["general"]["timeformat"]
        self.timezone = config["general"]["timezone"]

    def insert_in_document(self, document_id, insert_payload):
        params = {
            "document_id": document_id,
            "insert_payload": insert_payload
        }
        requests.get(self.google_service_url + "/insert_in_document", params = params)

    def insert_in_document_kwargs(self, **kwargs):
        requests.get(self.google_service_url + "/insert_in_document", params = kwargs)

    def clear_document_content(self, document_id):
        params = {
            "document_id": document_id
        }
        requests.get(self.google_service_url + "/clear_document_content", params = params)

    def get_document_content(self, document_id):
        params = {
            "document_id": document_id
        }
        return requests.get(self.google_service_url + "/get_document_content", params = params)
    
    def get_calendar_items(self, calendar_names=[], items_to_ignore=[], timeformat="24h", timezone=None):
        params = {
            "calendar_names": calendar_names or self.calendar_names,
            "items_to_ignore": items_to_ignore or self.items_to_ignore,
            "timeformat": timeformat or self.timeformat,
            "timezone": timezone or self.timezone
        }
        return requests.get(self.google_service_url + "/get_calendar_items", params = params)
