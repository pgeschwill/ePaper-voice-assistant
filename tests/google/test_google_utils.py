from services.google import google_utils
from os import path

class TestGoogleUtils:

    def test_get_calendar_events_empty_events_list(self):
        # ARRANGE
        events_list = {'items': []}
        items_to_ignore = []

        # ACT
        actual_events = google_utils.get_calendar_events(events_list, items_to_ignore)

        # ASSERT
        expected_events = {}
        assert actual_events == expected_events

    def test_get_calendar_events_no_items_to_ignore(self):
        # ARRANGE
        events_list = {
            'items': [
                {'summary': 'Event1', 'start': {'dateTime': '2024-02-15T10:00:00'}},
                {'summary': 'Event2', 'start': {'dateTime': '2024-02-15T12:00:00'}}
            ]
        }
        items_to_ignore = []

        # ACT
        actual_events = google_utils.get_calendar_events(events_list, items_to_ignore)

        # ASSERT
        expected_events = {
            '2024-02-15T10:00:00-0': {'summary': 'Event1', 'start': {'dateTime': '2024-02-15T10:00:00'}},
            '2024-02-15T12:00:00-0': {'summary': 'Event2', 'start': {'dateTime': '2024-02-15T12:00:00'}}
        }
        assert actual_events == expected_events

    def test_get_calendar_events_ignore_specific_events(self):
        # ARRANGE
        events_list = {
            'items': [
                {'summary': 'Event1', 'start': {'dateTime': '2024-02-15T10:00:00'}},
                {'summary': 'Event2', 'start': {'dateTime': '2024-02-15T12:00:00'}}
            ]
        }
        items_to_ignore = ['Event1']

        # ACT
        actual_events = google_utils.get_calendar_events(events_list, items_to_ignore)

        # ASSERT
        expected_events = {
            '2024-02-15T12:00:00-0': {'summary': 'Event2', 'start': {'dateTime': '2024-02-15T12:00:00'}}
        }
        assert actual_events == expected_events

    def test_get_calendar_events_events_with_same_start_time(self):
        # ARRANGE
        events_list = {
            'items': [
                {'summary': 'Event1', 'start': {'dateTime': '2024-02-15T10:00:00'}},
                {'summary': 'Event2', 'start': {'dateTime': '2024-02-15T10:00:00'}}
            ]
        }
        items_to_ignore = []

        # ACT
        actual_events = google_utils.get_calendar_events(events_list, items_to_ignore)

        # ASSERT
        expected_events = {
            '2024-02-15T10:00:00-0': {'summary': 'Event1', 'start': {'dateTime': '2024-02-15T10:00:00'}},
            '2024-02-15T10:00:00-1': {'summary': 'Event2', 'start': {'dateTime': '2024-02-15T10:00:00'}}
        }
        assert actual_events == expected_events

    def test_parse_calendar_events_12h_timeformat(self):
        # ARRANGE
        events = {
            '2024-02-15T10:00:00-0': {'summary': 'Event1', 'start': {'dateTime': '2024-02-15T10:00:00'}, 'end': {'dateTime': '2024-02-15T12:00:00'}}
        }
        timeformat = "12h"

        # ACT
        actual_calendar_items = google_utils.parse_calendar_events(events, timeformat)

        # ASSERT
        expected_calendar_items = [{
            "start_date": '02-15',
            "end_date": '02-15',
            "start_time": '10:00 AM',
            "end_time": '12:00 PM',
            "content": 'Event1',
            "week": 7
        }]
        assert actual_calendar_items == expected_calendar_items

    def test_parse_calendar_events_24h_timeformat(self):
        # ARrANGE
        events = {
            '2024-02-15T14:30:00-0': {'summary': 'Event2', 'start': {'dateTime': '2024-02-15T14:30:00'}, 'end': {'dateTime': '2024-02-15T16:30:00'}}
        }
        timeformat = "24h"

        # ACT
        actual_calendar_items = google_utils.parse_calendar_events(events, timeformat)

        # ASsERT
        expected_calendar_items = [{
            "start_date": '15.02.',
            "end_date": '15.02.',
            "start_time": '14:30',
            "end_time": '16:30',
            "content": 'Event2',
            "week": 7
        }]
        assert actual_calendar_items == expected_calendar_items

    def test_parse_calendar_events_multiple_events(self):
        # ARRANGE
        events = {
            '2024-02-15T10:00:00-0': {'summary': 'Event1', 'start': {'dateTime': '2024-02-15T10:00:00'}, 'end': {'dateTime': '2024-02-15T12:00:00'}},
            '2024-02-16T15:30:00-0': {'summary': 'Event2', 'start': {'dateTime': '2024-02-16T15:30:00'}, 'end': {'dateTime': '2024-02-16T17:30:00'}}
        }
        timeformat = "12h"

        # ACT
        actual_calendar_items = google_utils.parse_calendar_events(events, timeformat)

        # ASSERT
        expected_calendar_items = [
            {
                "start_date": '02-15',
                "end_date": '02-15',
                "start_time": '10:00 AM',
                "end_time": '12:00 PM',
                "content": 'Event1',
                "week": 7
            },
            {
                "start_date": '02-16',
                "end_date": '02-16',
                "start_time": '03:30 PM',
                "end_time": '05:30 PM',
                "content": 'Event2',
                "week": 7
            }
        ]
        assert actual_calendar_items == expected_calendar_items