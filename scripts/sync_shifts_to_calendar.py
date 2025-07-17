import os
import json
import re
from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- 設定 ---
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CALENDAR_ID = 'ten.ten.tenma.goal@gmail.com' # ボスのGoogleアカウントのメールアドレスに修正してください
SHIFTS_FILE_PATH = 'Tasks/Shifts.md' # シフトファイルへのパス

def get_credentials():
    """GitHub Secretsからサービスアカウントの認証情報を取得する"""
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if not credentials_json:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set.")
    info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return credentials

def parse_shifts_from_markdown(file_path):
    """Markdownのシフトファイルを解析してシフトイベントのリストを返す"""
    shifts = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Shift file not found at {file_path}")
        return []

    # 各行を解析
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue

        # フォーマット例:
        # シフト: YYYY-MM-DD シフト名 (例: 早番, 遅番, 休み)
        # シフト: YYYY-MM-DD HH:MM-HH:MM
        
        # 時間指定シフトの正規表現
        time_shift_match = re.match(r"シフト:\s*(\d{4}-\d{2}-\d{2})\s*(\d{2}:\d{2})-(\d{2}:\d{2})", line)
        # 終日シフト（シフト名または休み）の正規表現
        all_day_shift_match = re.match(r"シフト:\s*(\d{4}-\d{2}-\d{2})\s*(.+)", line)

        if time_shift_match:
            date_str, start_time_str, end_time_str = time_shift_match.groups()
            shift_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_datetime = datetime.strptime(f"{date_str} {start_time_str}", '%Y-%m-%d %H:%M')
            end_datetime = datetime.strptime(f"{date_str} {end_time_str}", '%Y-%m-%d %H:%M')
            
            shifts.append({
                'summary': f"シフト: {start_time_str}-{end_time_str}",
                'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'Asia/Tokyo'},
                'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'Asia/Tokyo'},
                'is_all_day': False
            })
        elif all_day_shift_match:
            date_str, shift_name = all_day_shift_match.groups()
            shift_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            shifts.append({
                'summary': f"シフト: {shift_name.strip()}",
                'start': {'date': shift_date.isoformat()},
                'end': {'date': (shift_date + timedelta(days=1)).isoformat()},
                'is_all_day': True
            })
        else:
            print(f"Warning: Could not parse shift line: '{line}'. Skipping.")
            
    return shifts

def create_google_calendar_event(service, event_body):
    """Googleカレンダーにイベントを作成する"""
    try:
        print(f"Attempting to create event '{event_body.get('summary')}' on calendar '{CALENDAR_ID}'...")
        event = service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()
        print(f"Event created: {event.get('htmlLink')} for '{event_body.get('summary')}'")
    except HttpError as error:
        print(f"An error occurred: {error} for '{event_body.get('summary')}'")

def main():
    print("Starting Google Calendar shift sync script...")
    try:
        credentials = get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
    except Exception as e:
        print(f"Failed to get Google API credentials or build service: {e}")
        return

    shifts_to_sync = parse_shifts_from_markdown(SHIFTS_FILE_PATH)
    
    if not shifts_to_sync:
        print("No shifts found to sync.")
        return

    print(f"Found {len(shifts_to_sync)} shifts. Checking existing events on calendar '{CALENDAR_ID}'...")

    # 既存のイベントを取得し、重複登録を避ける
    # 今日から未来のイベントを検索 (過去のシフトは同期しない)
    now = datetime.utcnow().isoformat() + 'Z' 
    
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                          maxResults=250, singleEvents=True,
                                          orderBy='startTime').execute()
    existing_events = events_result.get('items', [])
    existing_summaries = {event['summary'] for event in existing_events}

    for shift in shifts_to_sync:
        shift_summary = shift['summary']

        if shift_summary not in existing_summaries:
            create_google_calendar_event(service, shift)
        else:
            print(f"Shift '{shift_summary}' already exists in calendar '{CALENDAR_ID}'. Skipping.")

    print("Google Calendar shift sync script finished.")

if __name__ == '__main__':
    main()
