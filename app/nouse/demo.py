from __future__ import print_function
# Create your views here.
import datetime
import os.path
from uuid import uuid4

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('app/credentials/token.json'):
        creds = Credentials.from_authorized_user_file(
            'app/credentials/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'app/credentials/desktop.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('app/credentials/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        ev = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2022-12-31T09:00',
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': '2022-12-31T17:00',
                'timeZone': 'Asia/Kolkata',
            },
            "conferenceData": {"createRequest": {"requestId": str(uuid4()), "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
            }

        ev = service.events().insert(calendarId='primary', body=ev,conferenceDataVersion=1).execute()
        print('Event created: %s' % (ev.get('htmlLink')))

        # {'kind': 'calendar#event', 'etag': '"3344775111872000"', 'id': '07cmmn5vd8a9e8k69lbn34477j', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MDdjbW1uNXZkOGE5ZThrNjlsYm4zNDQ3N2ogcGFsbGF2cmFqMjMxMDIwMDBAbQ', 'created': '2022-12-30T08:05:55.000Z', 'updated': '2022-12-30T08:05:55.936Z', 'summary': 'new', 'creator': {'email': 'pallavraj23102000@gmail.com', 'self': True}, 'organizer':
        #  {'email': 'pallavraj23102000@gmail.com', 'self': True}, 'start': {'dateTime': '2022-12-31T06:30:00+05:30', 'timeZone': 'UTC'}, 'end': {'dateTime': '2022-12-31T07:30:00+05:30', 'timeZone': 'UTC'}, 'iCalUID': '07cmmn5vd8a9e8k69lbn34477j@google.com', 'sequence': 0, 'hangoutLink': 'https://meet.google.com/asp-vrxg-eka', 'conferenceData': {'entryPoints': [{'entryPointType': 'video', 'uri': 'https://meet.google.com/asp-vrxg-eka', 'label': 'meet.google.com/asp-vrxg-eka'}], 'conferenceSolution': {'key': {'type': 'hangoutsMeet'}, 'name': 'Google Meet', 'iconUri': 'https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png'}, 'conferenceId': 'asp-vrxg-eka'}, 'reminders': {'useDefault': True}, 'eventType': 'default'}

        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event)

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
