# Zettelkasten-Notes - Project-Specific Rules

## 目次
1. [Core Principles (絶対遵守原則)](#1-core-principles-絶対遵守原則)
2. [Directory Structure Principles (ディレクトリ構造の原則)](#2-directory-structure-principles-ディレクトリ構造の原則)
3. [Specific Conventions (個別規約)](#3-specific-conventions-個別規約)
   - [SC-01: Information Capture & Triage Workflow](#sc-01-information-capture--triage-workflow)
   - [SC-02: Note Formatting & Naming Conventions](#sc-02-note-formatting--naming-conventions)
   - [SC-03: Knowledge Management](#sc-03-knowledge-management)

## 1. Core Principles (絶対遵守原則)

- **P-01: 即時コミット原則:** ファイルの作成、更新、削除を行った後は、関連する変更をすべてリポジトリにコミットし、プッシュして最新の状態を維持すること。
- **P-02: 安全なコミットメッセージ原則:** `git commit`を実行する際は、コミットメッセージを一時的なテキストファイル（`temp_commit_message.txt`）に書き出し、`git commit -F <file>`の形式で安全に渡すこと。
- **P-03: 仕様とドキュメントの同期原則:** 仕様（ワークフロー、ルールなど）を変更した際は、関連する全てのドキュメント（グローバル、ローカルの`GEMINI.md`など）を必ず同時に更新し、一貫性を維持すること。
- **P-04: プロセス品質原則:** ファイルの削除を含む`Inflow`整理プロセス全体がスムーズかつ完璧であることを期待されている。
- **P-05: リポジトリコンテキスト指定原則:** `run_shell_command`で`git`コマンドを実行する際は、必ず`-C Zettelkasten-Notes`オプションを付与し、操作対象のリポジトリを明示的に指定すること。これにより、実行カレントディレクトリに依存しない、安定した操作を保証する。

## 2. Directory Structure Principles (ディレクトリ構造の原則)

このリポジトリは、情報の性質に応じて分類する**PARAメソッド**を基本思想として採用する。

- **`10_Projects/`**: **プロジェクト** -「完了」という明確な目標と期限を持つ活動。
  - 例: `JobHunt`, `DevIdeas`
- **`20_Areas/`**: **エリア** - 長期的に維持・向上させていく責任範囲や関心事。
  - 例: `SelfAnalysis`, `Health` (もしあれば)
- **`30_Resources/`**: **リソース** - 特定のテーマに関する知識や情報の蓄積場所。ツェッテルカステンの本体。
  - 例: `FleetingNote`, `LiteratureNote`, `PermanentNote`
- **`40_Archives/`**: **アーカイブ** - 上記3つで終了したもの、および`Inflow`のような一時的な置き場。
  - 例: `Inflow`, `Tasks`, `scripts`

## 3. Specific Conventions (個別規約)

### SC-01: Information Capture & Triage Workflow

- **唯一の入り口:** すべての情報は、まず`40_Archives/Inflow/_QuickCapture.md`に集約する。
- **定期的な仕分け (Triage):** `Inflow`内の情報は、週に一度などの頻度でレビューし、以下のいずれかのアクションを実行する。
    1.  関連するプロジェクト(`10_Projects`)、エリア(`20_Areas`)、リソース(`30_Resources`)のいずれかにノートとして移動・昇華させる。
    2.  具体的なタスクであれば、`40_Archives/Tasks/`配下の適切なファイルに転記する。
    3.  不要であれば、その場で削除する。
- **`Inflow`の空虚化:** 定期的な仕分けにより、`Inflow`は常に空に近い状態を維持する。

### SC-02: Note Formatting & Naming Conventions

- **ファイル命名規則:**
    - **基本形:** `カテゴリ_トピック.md` または `YYYY-MM-DD_トピック.md` の形式を推奨する。
    - **区切り文字:** 単語の区切りには、スペースやハイフンではなく、アンダースコア `_` を使用する。
- **`DevIdeas`のフォーマット:** `DevIdeas`フォルダ内のファイルは、H1タイトルの下に「タグ」を設け、内容は「## H2見出し」と箇条書きリストで構成する。Calloutやチェックボックスは使用しない。
- **`CompanyResearch`の必須項目:** `CompanyResearch`ノート作成時は、以下の項目を必ず網羅する。
    - 企業概要（会社名、設立、代表者、資本金、売上高、従業員数、本社所在地、主な株主、事業内容）
    - 企業理念・ビジョン・バリュー
    - 事業・製品・サービス
    - 働き方・文化
    - 勤務地
    - 待遇・福利厚生(初任給含む)
    - 求める人物像
    - メモ・考察

### SC-03: Knowledge Management

- **ノートの関連付け:** ファイルには、内容の関連性に応じてタグと双方向リンクを適宜付与し、知識のネットワークを強化する。
- **MOCの定期的な整理:** Map of Content (MOC) は、知識の体系化と発見性を高めるために、適宜整理し、最新の状態を保つ。