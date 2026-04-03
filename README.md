# 🎙️ AI リアルタイム議事録・翻訳アシスタント (AI Meeting Assistant)

留学生やビジネスパーソンのために開発された、リアルタイム音声文字起こし及び翻訳ツールです。

---

## 🌟 開発背景 (Background)
日本での学生生活において、スピードの速い講義内容をリアルタイムで完全に理解することは大きな挑戦です。この課題を解決するため、生成AI（Whisper & GPT）を活用し、音声を即座にテキスト化・翻訳して記録に残せるツールを開発しました。

## 🚀 主な機能 (Features)
- **リアルタイム文字起こし & 翻訳**: マイク入力から4秒ごとに音声を切り出し、Whisperでテキスト化、GPTで翻訳を同時進行します。
- **ファイルアップロード解析**: 既存の音声ファイル（MP3/WAV/M4A）をアップロードし、一括で議事録を作成します。
- **履歴管理システム**:
    - **データ永続化**: 翻訳結果を JSON/TXT 形式でローカルに保存。
    - **音声録音の紐付け**: テキストだけでなく、録音データも同時に保存し、履歴からいつでも再生可能。
    - **削除機能**: 不要になったデータをサイドバーから簡単に削除可能。

## 🛠️ 技術スタック (Tech Stack)
- **Frontend**: Streamlit
- **AI Models**: 
    - OpenAI Whisper API (音声認識)
    - OpenAI GPT-4o API (翻訳・要約)
- **Library**: `audio-recorder-streamlit`, `python-dotenv`
- **Infrastructure**: Local File System (JSON & WAV storage)

## 📸 スクリーンショット (Screenshots)
![Main UI](`docs`/home.png)
![Upload UI](`docs`/upload.png)
![History UI](`docs`/history.png)

## ⚙️ セットアップ (Installation)
1. **リポジトリをクローン**
    ```bash
   git clone https://github.com/linlin888-666/AI-Meeting-Assistant.git
   cd Meeting_AI

## システムアーキテクチャ（System Architecture）
![System Architecture](`docs`/System_Architecture.png)

## 📁 ディレクトリ構成（Project Structure）
```text
MEETING_AI/                          # プロジェクトルート
├── app.py                           # メインエントリーポイント
├── style.py 　　　　                # UIのデザイン
├── `docs`　　　                     # 写真
├── requirements.txt                 # 依存パッケージ一覧
├── .env                             # 環境変数
├── .gitignore                       # Git除外設定（アップロードしないファイル指定）
├── README.md                        # プロジェクト説明書
│
├── components/                      # UIコンポーネント
│   ├── __init__.py                  # パッケージ初期化
│   ├── home.py                      # ホーム画面
│   ├── live.py                      # リアルタイム録音画面
│   └── upload.py                    # ファイルアップロード画面
│
├── utils/                           # ユーティリティ（共通機能・便利関数を集約）
│   ├── __init__.py                  # パッケージ初期化
│   ├── ai_handler.py                # AI API連携
├── saved_records/                   # 永続化ストレージ
│   └── (JSONファイル等)              # 生成された議事録データ（自動作成）
```

### 依存パッケージのインストール
- pip install -r requirements.txt

### 環境変数の設定
#### ルートディレクトリに .env ファイルを作成し、APIキーを設定してください。
- OPENAI_API_KEY=あなたのAPIキー

### アプリの起動
- streamlit run app.py

