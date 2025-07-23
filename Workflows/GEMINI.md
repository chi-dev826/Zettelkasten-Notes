---
title: "GEMINI WORKFLOWS - BOSS COMPLETE v4"
author: "ボス"
version: "4.0.0"
updated: "2025-07-15"

workflows:
  - id: summarize_inflow_to_daily
    description: "Inflow/_QuickCapture.mdからアイデアやメモを解析し、Dailyや各ノートに追記・整理する。ハイブリッド・クイックキャプチャの中核。"
    input_file: "Inflow/_QuickCapture.md"
    steps:
      - read_and_classify_fragments:
          source_file: "Inflow/_QuickCapture.md"
          categories: ["memo", "idea", "reflection", "todo", "reference", "devidea", "university_task", "shift", "general_task"]
          instruction: |
            接頭辞（todo:, memo:, 大学タスク:, シフト:, タスク:など）や内容に基づき、各フラグメントを分類せよ。
      - process_fragments:
          instruction: |
            分類に基づき、以下の処理を実行せよ。
            - todo: 今日のDailyNoteのToDoセクションに追記。
            - memo, idea, reflection: 今日のDailyNoteの各セクションに追記。
            - reference: URLをDailyNoteの参照セクションに記載、またはLiteratureNote作成を提案。
            - devidea: DevIdeasフォルダに新しいノートとして起票。
            - university_task: Tasks/University.mdの表形式に追記/更新。
            - shift: Tasks/Shifts.mdに行として追記。
            - general_task: Tasks/General.mdにチェックボックス形式で追記。
      - clear_processed_file:
          file: "Inflow/_QuickCapture.md"
          instruction: "処理が完了したため、_QuickCapture.mdの中身を空にせよ。"
      - commit_changes:
          instruction: "処理された変更をGitにコミットし、プッシュせよ。コミットメッセージは動的に生成され、一時ファイル（temp_commit_message.txt）経由で安全に渡される。"

  - id: manage_tasks
    description: "Dailyノートのタスクを管理（完了タスクの削除、期限抽出）。Inflowからの直接追加は廃止。"
    steps:
      - process_completed_todos:
          instruction: "Dailyノート内の「- [x]」とマークされたタスクをアーカイブまたは削除せよ。"
      - extract_deadlines:
          instruction: "Dailyノート内のタスクから期限情報を抽出し、カレンダー連携などに活用せよ。"

  - id: create_literature_note_from_daily
    description: "DailyノートのURLから要約と知見を抽出しLiteratureNoteを作成。"
    input_dir: "Daily/"
    output_dir: "LiteratureNote/"

  - id: process_clipped_notes
    description: "Obsidian Web ClipperでクリップされたファイルをZettelkasten-Notes/LiteratureNoteに移動し、処理後に元のファイルを削除する。"
    input_dir: "../Clippings/"
    output_dir: "LiteratureNote/"
    steps:
      - scan_directory:
          dir: "../Clippings/"
      - add_literature_note_tags:
          instruction: |
            クリップされたファイルに、文献ノートとして適切なタグを付与せよ。
      - move_files:
          destination_dir: "LiteratureNote/"
      - delete_processed_files: true

  - id: draft_permanent_note
    description: "FleetingNoteとLiteratureNoteを横断してPermanentNoteを生成"
    input_dirs: ["FleetingNote/", "LiteratureNote/"]
    output_dir: "PermanentNote/"

  - id: create_github_issues_from_devideas
    description: "DevIdeasからGitHub Issueの草案を生成"
    input_dirs: ["Daily/", "LiteratureNote/"]
    output_dir: "DevIdeas/"

  - id: research_company
    description: "指定企業をWeb検索し、CompanyResearchノートを作成"
    input_var: "company"
    output_file: "JobHunt/CompanyResearch/{company}.md"

  - id: draft_es_from_experience_and_company
    description: "自己経験と企業情報からESを生成"
    input_files:
      - "JobHunt/Experience/{today}.md"
      - "JobHunt/CompanyResearch/{company}.md"
    output_file: "JobHunt/Drafts/{company}_ES_{today}.md"

  - id: update_index_note
    description: "PermanentNoteやCompanyResearchをIndexNoteに反映"
    source_dirs:
      - "PermanentNote/"
      - "JobHunt/CompanyResearch/"
    output_files:
      - "IndexNote/Permanent_Index.md"
      - "IndexNote/Company_Index.md"

  - id: self_analysis_from_daily_and_selfknowledge
    description: "DailyとSelfKnowledgeから自己分析を行い、SelfAnalysisへ出力。"
    input_dirs:
      - "Daily/"
      - "SelfKnowledge/"
    output_dir: "SelfAnalysis/"
    steps:
      - extract_fragments:
          instruction: |
            感情・価値観・行動・思考の記述を抽出
      - analyze_self:
          instruction: |
            次の観点でユーザーを分析：
            1. 思考の癖
            2. 強み
            3. 弱み・回避傾向
            4. 大切にしている価値観
            5. 成長観・仕事観
            6. 動機の源泉
      - write_to_file:
          filename_template: "summary_{today}.md"

  - id: manage_shifts
    description: "Inflowフォルダからシフト情報を抽出し、Tasks/Shifts.mdに整理。"
    input_dir: "Inflow/"
    output_file: "Tasks/Shifts.md"
    append: true
    steps:
      - scan_directory:
          dir: "Inflow/"
      - extract_shifts_from_inflow:
          instruction: "Inflow内の「シフト: YYYY-MM-DD シフト名」または「シフト: YYYY-MM-DD HH:MM-HH:MM」形式の行を抽出し、日付、時間、シフト名を解析せよ"
      - update_shift_file:
          instruction: "抽出したシフト情報をTasks/Shifts.mdに追記または更新せよ。重複は避けること。"
      - delete_processed_files: true

  - id: add_event_to_calendar
    description: "Clippingsや手動での情報からイベントを作成し、Googleカレンダーに自動同期する。"
    input_dir: "Clippings/"
    output_file: "Tasks/Events.md"
    steps:
      - extract_event_info:
          instruction: "Clippings内のファイルやユーザーの指示から、イベント名、日付、時刻を抽出せよ。"
      - format_and_append_event:
          target_file: "Tasks/Events.md"
          instruction: "抽出した情報を `- [ ] {イベント名} YYYY-MM-DD HH:MM` の形式で Tasks/Events.md に追記せよ。"
      - commit_and_push:
          instruction: "変更をGitにコミット＆プッシュせよ。これにより、GitHub Actionsがトリガーされ、Googleカレンダーに同期される。"

---

# GEMINI CLI ワークフロー定義（ver.4）

このファイルは、ボスの知的生産、自己理解、開発戦略、就活準備を支える統合ワークフローマネジメントです。

## ディレクトリ構成（最新版）

このワークフローは、基本的に`Zettelkasten-Notes`ディレクトリを基準に動作しますが、一部のワークフローはVaultのルートディレクトリを参照します。

```
. (Obsidian Vault Root)
├── Clippings/              # ✅ Web Clipperの自動保存先 (ワークフローがここを読み取る)
└── Zettelkasten-Notes/
    ├── Daily/
    ├── DevIdeas/
    ├── FleetingNote/
    ├── IndexNote/
    ├── Inflow/                 # ✅ _QuickCapture.md (単一の入力ゲートウェイ)
    ├── JobHunt/
    ├── LiteratureNote/     # ✅ Clippingsからの移動先
    ├── PermanentNote/
    ├── SelfAnalysis/
    ├── SelfKnowledge/
    ├── Tasks/
    └── Workflows/
        └── GEMINI.md       # このワークフロー定義ファイル
```



---

# 実行例（自然言語ベース）

- `gemini run quick_capture_process`
- `gemini run self_analysis`
- `gemini run update_moc`

