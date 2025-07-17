---
title: "GEMINI WORKFLOWS - BOSS COMPLETE v4"
author: "ボス"
version: "4.0.0"
updated: 2025-07-15

workflows:
  - id: summarize_inflow_to_daily
    description: "Inflowフォルダからアイデアやメモを要約し、Dailyに追記. タスクはmanage_tasksで処理（タスクとtodoの違い：タスクは主に学校に関することや就活に関する内容. todoは日常生活に関すること）"
    input_dir: "Inflow/"
    output_file: "Daily/{today}.md"
    append: true
    steps:
      - scan_directory:
          dir: "Inflow/"
      - classify_fragments:
          categories: ["url", "memo", "idea", "reflection", "todo"]
      - manage_todo:
          instruction: |
            todoにはチェックボックスを付与すること
      - fetch_urls:
          instruction: |
            URLを抽出し、Dailyに参照として記載せよ（詳細な要約はLiteratureNoteで）
      - summarize_free_text:
          instruction: |
            テキストから断片的思考やメモを抽出し、Dailyに追記せよ（URLの内容ではない）
      - write_to_file:
          filename_template: "{today}.md"
          mode: "append"
          section_headers: true
      - delete_processed_files: true

  - id: manage_tasks
    description: "Dailyノートのタスクを管理（Inflowからの追加、完了タスクの削除、期限抽出）. 一つのファイルでリスト形式で管理."
    input_dir: "Inflow/"
    output_dir: "Tasks/
    append: true
    steps:
      - scan_directory:
          dir: "Inflow/"
      - extract_todos_from_inflow:
          instruction: "Inflow内のタスク項目を抽出し、期限があればそれも抽出せよ"
      - process_completed_todos:
          instruction: "Tasksディレクトリ内の「〇〇完了」とマークされたタスクを削除せよ"
      - delete_processed_files: true

  - id: create_literature_note_from_daily
    description: "Dailyノートのurlから要約と知見を抽出しLiteratureNoteを作成。要約を端折りすぎないこと。"
    input_dir: "Daily/"
    output_dir: "LiteratureNote/"

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
    description: "DailyとSelfKnowledgeから自己分析を行い、SelfAnalysisへ出力"
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
    description: "Inflowフォルダからシフト情報を抽出し、Tasks/Shifts.mdに整理。カレンダー同期の準備。"
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

---

# GEMINI CLI ワークフロー定義（ver.4）

このファイルは、ボスの知的生産、自己理解、開発戦略、就活準備を支える統合ワークフローマネジメントです。

## ディレクトリ構成（最新版）

```
.
├── Inflow/                 # 投げ込みメモ、URL、思考断片（未整理の一次情報）
├── Daily/                  # 日次記録（その日の活動、簡易ToDo、高レベルな気づき。Inflowから整理された情報への参照）
├── LiteratureNote/         # 外部資料の要約・知見（URLや文献の詳細な要約と考察。主題に関する詳細なタグ付け）
├── FleetingNote/           # 一時的な気づき・構想（まだ未整理のアイデアや思考の断片）
├── PermanentNote/          # 永続的な概念・知識（FleetingやLiteratureを統合し、普遍的な知識として昇華。抽象的なタグ付け）
├── DevIdeas/               # 開発アイデアや技術構想（プロジェクト、機能、バグなど開発に関する具体的な要素）
├── JobHunt/
│   ├── CompanyResearch/    # 企業分析結果（企業情報、求める人物像など就職活動の具体的な要素）
│   ├── Experience/         # 体験ベースの棚卸し（自己PRやESの元となる具体的な経験談）
│   └── Drafts/             # ESや志望動機草案（企業情報と自己経験を基に生成された下書き）
├── SelfKnowledge/          # 価値観・信念・過去の蓄積（自己分析の元となる価値観、強み、弱み、過去の記録）
├── SelfAnalysis/           # 自己分析の生成物（DailyやSelfKnowledgeを元に自動生成された自己分析結果）

```

## 必読

- summarize_inflow_to_dailyでは、適切に情報を仕分けすることが求められる
- ボスの手書きテキストとURLの内容を正確に識別すること（DialyノートにURLの内容を含めないため）
- すべてのファイルにタグを付与すること
- 基本的には"キーワード"ではなく、その"内容"に焦点を当てること
- Dialyノートには文献に関するタグやtodoに関するタグを付与しないこと. カテゴリ名をタグに含めないこと
- 文献ノートには文献に関する"キーワード"に焦点を当てること（例：AI, React, Cursor）
- 生成するファイルには適宜アイコンなどを用いて視覚的にわかりやすい内容を心がけること（以前のファイルを一つ読み込んで形式を揃えること）
- タスク管理表は適宜わかりやすく加工すること

---

# 実行例（自然言語ベース）

- `gemini run inflow整理して`
- `gemini run 自己分析まとめて`
- `gemini run アルバイトIndex作って`
- `gemini run タスク管理して`

