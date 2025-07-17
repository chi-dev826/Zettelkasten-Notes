import os
import json
import re
from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- 設定 ---
# Google Calendar APIのスコープ
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
# カレンダーID (通常は 'primary' でOK)
# CALENDAR_ID = 'primary' # コメントアウトまたは削除
CALENDAR_ID = 'ten.ten.tenma.goal@gmail.com' # ここをボスのGoogleアカウントのメールアドレスに修正 (既に修正済みのはず)
# タスクファイルへのパス (GitHub Actionsで実行されることを想定し、ルートからの相対パス)
TASKS_FILE_PATH = 'Tasks/University.md'

def get_credentials():
    """GitHub Secretsからサービスアカウントの認証情報を取得する"""
    # 環境変数からJSON文字列を取得
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if not credentials_json:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set.")

    # JSON文字列を辞書に変換
    info = json.loads(credentials_json)

    # サービスアカウントの認証情報を作成
    credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return credentials

def parse_markdown_tasks(file_path):
    """Markdownのタスクテーブルを解析して未完了のタスクリストを返す"""
    tasks = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Task file not found at {file_path}")
        return []

    # ヘッダー行と区切り行をスキップ
    lines = content.strip().split('\n')
    if len(lines) < 3: # ヘッダー、区切り、タスクが最低1行
        print("No tasks found or invalid format in the task file.")
        return []

    # | [ ] | Task Name | YYYY-MM-DD | の形式を解析
    # ステータスが '[ ]' (未完了) の行のみを対象
    task_pattern = re.compile(r"\|\s*\[\s*\]\s*\|\s*(.+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|")

    for line in lines[2:]: # ヘッダーと区切り行の次から読み込み
        match = task_pattern.match(line)
        if match:
            task_name = match.group(1).strip()
            due_date_str = match.group(2).strip()

            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                tasks.append({'name': task_name, 'due_date': due_date})
            except ValueError:
                print(f"Warning: Could not parse date '{due_date_str}' for task '{task_name}'. Skipping.")
    return tasks

def create_google_calendar_event(service, task_name, due_date):
    """Googleカレンダーにイベントを作成する"""
    # 終日イベントとして設定
    event = {
        'summary': task_name,
        'start': {
            'date': due_date.isoformat(),
        },
        'end': {
            'date': (due_date + timedelta(days=1)).isoformat(), # 終日イベントは翌日の0時まで
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 60 * 24}, # 1日前に通知
            ],
        },
    }

    try:
        # --- デバッグ情報追加 ---
        print(f"Attempting to create event '{task_name}' on calendar '{CALENDAR_ID}'...")
        # --- デバッグ情報追加 ---
        event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"Event created: {event.get('htmlLink')} for task '{task_name}'")
    except HttpError as error:
        print(f"An error occurred: {error} for task '{task_name}'")

def main():
    print("Starting Google Calendar sync script...")
    try:
        credentials = get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
    except Exception as e:
        print(f"Failed to get Google API credentials or build service: {e}")
        return

    # 未完了のタスクを解析
    incomplete_tasks = parse_markdown_tasks(TASKS_FILE_PATH)

    if not incomplete_tasks:
        print("No incomplete tasks found to sync.")
        return

    print(f"Found {len(incomplete_tasks)} incomplete tasks. Checking existing events on calendar '{CALENDAR_ID}'...") # デバッグ情報追加

    # 既存のイベントを取得し、重複登録を避ける
    # 今日から未来のイベントを検索
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    # --- デバッグ情報追加 ---
    print(f"Querying events from '{CALENDAR_ID}' starting from {now}...")
    # --- デバッグ情報追加 ---

    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                          maxResults=250, singleEvents=True,
                                          orderBy='startTime').execute()
    existing_events = events_result.get('items', [])

    # --- デバッグ情報追加 ---
    print(f"Found {len(existing_events)} existing events on calendar '{CALENDAR_ID}'.")
    for event in existing_events:
        print(f"  - Existing event: Summary='{event.get('summary')}', ID='{event.get('id')}'")
    # --- デバッグ情報追加 ---

    existing_summaries = {event['summary'] for event in existing_events}

    for task in incomplete_tasks:
        task_name = task['name']
        task_due_date = task['due_date']

        # 既にカレンダーに同じ名前のイベントが存在しないかチェック
        if task_name not in existing_summaries:
            create_google_calendar_event(service, task_name, task_due_date)
        else:
            print(f"Task '{task_name}' already exists in calendar '{CALENDAR_ID}'. Skipping.") # デバッグ情報追加

    print("Google Calendar sync script finished.")

if __name__ == '__main__':
    main()