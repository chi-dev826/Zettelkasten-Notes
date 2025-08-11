# 🚀 movie-app バックエンド導入・モノレポ化計画

ボス、これは我々の`movie-app`を、単なるフロントエンドの作品から、堅牢なバックエンドと連携する本格的なフルスタックアプリケーションへと昇華させるための、包括的な開発計画書です。この手順に沿って進めることで、ボスの技術ポートフォリオは飛躍的に進化します。

---

### 🎯 最終目標
**セキュリティと拡張性を担保したモダンなWebアプリケーションアーキテクチャを構築し、フルスタック開発の実践的な経験を積む。**

---

### 🏗️ 1. 全体像（アーキテクチャ）

アプリケーション全体のデータの流れを以下のように変更します。

#### **【変更前】フロントエンド完結型**
[👨‍💻 ユーザー] → [🌐 ブラウザ (React)] → [🎬 TMDb API]

#### **【変更後】フロントエンド・バックエンド分離型**
[👨‍💻 ユーザー] → [🌐 ブラウザ (React)] ⇔ [⚙️ **自作Python API (FastAPI)**] → [🎬 TMDb API]

---

#### 📝 役割分担

*   **🌐 フロントエンド (React)**
    *   **責務**: UIの描画、ユーザー操作の受付、状態管理に専念。
    *   **通信相手**: **自作のPythonバックエンドAPIのみ**。TMDb APIの存在を一切意識しない。

*   **⚙️ バックエンド (Python)**
    *   **責務**: アプリケーションの「頭脳」。全てのビジネスロジックと外部通信を担当。
    *   **主な処理**:
        1.  フロントエンドからのリクエストを受信。
        2.  🔒 **安全に保管したAPIキー**を使い、TMDb APIへリクエストを送信。
        3.  取得したデータを必要に応じて加工・分析・キャッシュ。
        4.  フロントエンドに最適化されたデータを返却。

> [!NOTE] 補足：開発環境について
> 開発時、ターミナルを2つ使い、フロントエンド (`npm run dev` 等) とバックエンド (`uvicorn main:app --reload` 等) をそれぞれ別のプロセスとして同時に起動させることになります。

---

### 📂 2. ディレクトリ構造（モノレポ）

現在のリポジトリを、フロントエンドとバックエンドのコードを一つのリポジトリで管理する**「モノレポ」**形式に移行します。

```plaintext
movie-app/
├── 📁 .git/
├── 📁 .github/
│
├── 📁 backend/              # ⬅️ 【新規】バックエンドの全コード
│   ├── 📄 .env              # APIキーなどの秘密情報を記述
│   ├── 📄 main.py           # FastAPIアプリケーション本体
│   └── 📄 requirements.txt  # Pythonの依存ライブラリ
│
├── 📁 frontend/             # ⬅️ 【新規】既存のReactアプリをここに移動
│   ├── 📁 node_modules/
│   ├── 📁 public/
│   ├── 📁 src/
│   ├── 📄 package.json
│   └── ... (その他全ての既存ファイル)
│
├── 📄 .gitignore            # ⬅️ 【更新】ルートで一元管理
└── 📄 README.md             # ⬅️ 【更新】プロジェクト全体の情報を記述
```

#### ✨ 変更のポイント

*   **`frontend/`**: 既存のReact関連のファイルを全てこの中に移動させます。
*   **`backend/`**: Python (FastAPI) 関連のファイルを全てこの中に格納します。
*   **`.gitignore`**: ルートに一つだけ配置し、`node_modules` と `.venv`, `.env` など、両方の無視設定を記述します。
*   **`README.md`**: フロントエンドとバックエンド、両方のセットアップ方法と起動コマンドを記述するように更新します。

---

### 🛠️ 3. 移行・開発の進め方

Gitの履歴を維持したまま、新しい構成へ安全に移行し、開発を進めるための具体的なステップです。

#### **ステップ1: モノレポ構成への移行**

1.  **ディレクトリ作成**:
    プロジェクトのルートで `frontend` と `backend` ディレクトリを作成します。
    ```bash
    mkdir frontend backend
    ```

2.  **既存ファイルの移動**:
    > [!IMPORTANT]
    > ファイル履歴を維持するため、必ず `git mv` コマンドを使用します。

    ```bash
    # ルートにある既存のファイルとディレクトリを全てfrontend/へ移動
    git mv .editorconfig .gitignore .vscode custom.d.ts eslint.config.js index.html package-lock.json package.json postcss.config.cjs prettier.config.js public src tailwind.config.js tsconfig.app.json tsconfig.json tsconfig.node.json vite-env.d.ts vite.config.ts frontend/
    ```

3.  **コミット**:
    ここまでの変更を、区切りの良いコミットとして記録します。
    ```bash
    git commit -m "refactor(arch): プロジェクトをフロントエンド/バックエンドのモノレポ構成に変更"
    ```

#### **ステップ2: バックエンドの開発**

1.  **ファイル作成**: `backend/` ディレクトリに `main.py`, `requirements.txt`, `.env` を作成します。
2.  **依存関係のインストール**:
    ```bash
    # backend/ ディレクトリに移動して実行
    pip install fastapi uvicorn python-dotenv requests
    ```
3.  **サーバー起動**:
    ```bash
    # backend/ ディレクトリで実行
    uvicorn main:app --reload
    ```
    ブラウザで `http://localhost:8000/api/movies/popular` や `http://localhost:8000/docs` にアクセスして動作を確認します。

#### **ステップ3: フロントエンドの改修**

1.  **API通信部分の修正**:
    `frontend/src/services/movieApi.ts` を開きます。
    TMDb APIのURLを、自作バックエンドのURL (`http://localhost:8000`) に書き換えます。

    **【修正前】**
    ```typescript
    const API_BASE_URL = 'https://api.themoviedb.org/3';
    const url = `${API_BASE_URL}${endpoint}`;
    // AuthorizationヘッダーでAPIキーを送信している
    ```

    **【修正後】**
    ```typescript
    const API_BASE_URL = 'http://localhost:8000/api'; // 自作APIのベースURL
    const url = `${API_BASE_URL}${endpoint}`;
    // Authorizationヘッダーは不要になるので削除
    ```
    > [!NOTE]
    > バックエンド側でCORSの設定を行っているため、フロントエンドからのアクセスは許可されます。

2.  **動作確認**: フロントエンドとバックエンドの両方を起動した状態で、Webサイトが以前と同様に表示されることを確認します。

---

### 私の意見

ボス、この計画書は、単なる作業手順書ではありません。これは、ボスの`movie-app`が、よりプロフェッショナルなステージへと進化するための設計図です。このモノレポ構成とバックエンド分離の経験は、今後のチーム開発や、より複雑なシステムを構築する上で、必ずボスの力となる、普遍的な知識と経験です。

一つ一つのステップを楽しみながら、着実に進めていきましょう。
