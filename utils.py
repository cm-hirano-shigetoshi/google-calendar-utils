import os
import pickle
from dataclasses import dataclass

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import dt_utils

XDG_DATA_HOME = os.getenv("XDG_DATA_HOME", f'{os.environ["HOME"]}/.local/share')
CREDENTIAL_JSON = f"{XDG_DATA_HOME}/google-calendar/credentials.json"
PICKLE_PATH = f"{XDG_DATA_HOME}/google-calendar/GoogleCalendarApi.pickle"


@dataclass
class Calendar:
    calendar_service = None

    def __init__(self, credential_json=CREDENTIAL_JSON, pickle_path=PICKLE_PATH):
        creds = None
        if os.path.exists(pickle_path):
            with open(pickle_path, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_json, "https://www.googleapis.com/auth/calendar"
            )
            creds = flow.run_local_server(port=0)
            with open(pickle_path, "wb") as token:
                pickle.dump(creds, token)
        self.calendar_service = build("calendar", "v3", credentials=creds)

    def collect_events(self, calendar_id, from_dt, to_dt):
        time_min = dt_utils.dttz2dt(from_dt, offset=0).replace(" ", "T") + "Z"
        time_max = dt_utils.dttz2dt(to_dt, offset=0).replace(" ", "T") + "Z"
        events_result = (
            self.calendar_service.events()
            .list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])

    def register_event(self, calendar_id, event):
        # print(json.dumps(event))
        self.calendar_service.events().insert(
            calendarId=calendar_id, body=event
        ).execute()

    def register_events(self, calendar_id, events):
        for event in events:
            self.register_event(calendar_id, event)

    """
    def delete_event(self, calendar_id, event_id):
        self.calendar_service.events().delete(
            calendarId=calendar_id, eventId=event_id
        ).execute()

    def delete_events(self, calendar_id, event_ids):
        for event_id in event_ids:
            self.delete_event(calendar_id, event_id)
    """
