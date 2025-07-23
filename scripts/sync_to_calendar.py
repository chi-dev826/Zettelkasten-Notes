import os
import json
import re
import sys
from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- 設定 ---
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CALENDAR_ID = 'ten.ten.tenma.goal@gmail.com'
TIMEZONE = 'Asia/Tokyo'

def get_credentials():
    """GitHub Secretsからサービスアカウントの認証情報を取得する"""
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if not credentials_json:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set.")
    info = json.loads(credentials_json)
    return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

def parse_university_tasks(content):
    """大学タスクのMarkdownテーブルを解析"""
    events = []
    task_pattern = re.compile(r"\|\s*\[\s*\]\s*\|\s*(.+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|")
    for line in content.strip().split('\n'):
        match = task_pattern.match(line)
        if match:
            task_name, due_date_str = match.groups()
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            events.append({
                'summary': task_name.strip(),
                'start': {'date': due_date.isoformat()},
                'end': {'date': (due_date + timedelta(days=1)).isoformat()},
            })
    return events

def parse_shifts(content):
    """シフトのテキスト形式を解析"""
    events = []
    for line in content.strip().split('\n'):
        line = line.strip()
        time_shift_match = re.match(r"シフト:\s*(\d{4}-\d{2}-\d{2})\s*(\d{2}:\d{2})-(\d{2}:\d{2})", line)
        all_day_shift_match = re.match(r"シフト:\s*(\d{4}-\d{2}-\d{2})\s*(.+)", line)

        if time_shift_match:
            date_str, start_time_str, end_time_str = time_shift_match.groups()
            start_datetime = datetime.strptime(f"{date_str} {start_time_str}", '%Y-%m-%d %H:%M')
            end_datetime = datetime.strptime(f"{date_str} {end_time_str}", '%Y-%m-%d %H:%M')
            events.append({
                'summary': f"シフト: {start_time_str}-{end_time_str}",
                'start': {'dateTime': start_datetime.isoformat(), 'timeZone': TIMEZONE},
                'end': {'dateTime': end_datetime.isoformat(), 'timeZone': TIMEZONE},
            })
        elif all_day_shift_match:
            date_str, shift_name = all_day_shift_match.groups()
            shift_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            events.append({
                'summary': f"シフト: {shift_name.strip()}",
                'start': {'date': shift_date.isoformat()},
                'end': {'date': (shift_date + timedelta(days=1)).isoformat()},
            })
    return events

def sync_events(service, events_to_sync):
    """カレンダーとイベントを同期"""
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                          maxResults=250, singleEvents=True,
                                          orderBy='startTime').execute()
    existing_events = {event['summary'] for event in events_result.get('items', [])}

    for event in events_to_sync:
        if event['summary'] not in existing_events:
            try:
                service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
                print(f"Event created: {event['summary']}")
            except HttpError as error:
                print(f"An error occurred: {error} for event '{event['summary']}'")
        else:
            print(f"Event '{event['summary']}' already exists. Skipping.")

def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print("Usage: python sync_to_calendar.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"Processing file: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    events = []
    if 'University.md' in file_path:
        print("Parsing as University tasks...")
        events = parse_university_tasks(content)
    elif 'Shifts.md' in file_path:
        print("Parsing as shifts...")
        events = parse_shifts(content)
    else:
        print("File not configured for calendar sync. Exiting.")
        sys.exit(0)

    if not events:
        print("No events to sync.")
        return

    try:
        credentials = get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
        sync_events(service, events)
    except Exception as e:
        print(f"An error occurred during Google API interaction: {e}")
        sys.exit(1)

    print("Sync script finished.")

if __name__ == '__main__':
    main()
