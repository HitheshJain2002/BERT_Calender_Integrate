import pandas as pd
import os
import re
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Helper function to remove ordinal suffixes from day numbers
def remove_ordinal_suffix(date_str):
    # Remove ordinal suffixes (st, nd, rd, th)
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    # Remove any extra brackets
    date_str = date_str.strip('[]')
    return date_str

# Load the CSV file
df = pd.read_csv('filtered_dates.csv')

# Authenticate with Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Build the Google Calendar service
service = build('calendar', 'v3', credentials=creds)

# Iterate through the rows of the DataFrame and create events
for index, row in df.iterrows():
    task_description = row['email_body']
    raw_dates = row['extracted_dates']

    # Check if multiple dates are present (comma-separated)
    dates_list = raw_dates.split(',')  # Split if multiple dates are present
    
    for raw_date in dates_list:
        # Preprocess each date to remove ordinal suffixes and parse
        clean_date = remove_ordinal_suffix(raw_date.strip())
        try:
            # Parse the cleaned date
            event_time = datetime.strptime(clean_date, "%d %B %Y")

            # Define event start and end times (default to 10:00 AM UTC for 1 hour)
            start_time = event_time.replace(hour=10)
            end_time = start_time + timedelta(hours=1)

            # Prepare the event details
            event = {
                'summary': 'Task from CSV',
                'description': task_description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }

            # Create the event in Google Calendar
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event created for task on {start_time} with ID: {created_event['id']}")

        except ValueError:
            print(f"Date format error for row {index}: '{raw_date}' - Unable to parse date.")
