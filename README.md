# 🎙️ AI リアルタイム議事録・翻訳アシスタント (AI Meeting Assistant)

留学生やビジネスパーソンのために開発された、リアルタイム音声文字起こし及び翻訳ツールです。

---

## 🌟 開発背景 (Background)
日本での学生生活において、スピードの速い講義内容をリアルタイムで完全に理解することは大きな挑戦です。この課題を解決するため、生成AI（Whisper & GPT）を活用し、音声を即座にテキスト化・翻訳して記録に残せるツールを開発しました。

## 🚀 主な機能 (Features)
- **リアルタイム文字起こし & 翻訳**: <br>
  マイク入力から4秒ごとに音声を切り出し、Whisperでテキスト化、GPTで翻訳を同時進行します。
- **ファイルアップロード解析**: <br>
  既存の音声ファイル（MP3/WAV/M4A）をアップロードし、一括で議事録を作成します。
- **履歴管理システム**:
    - **データ永続化**:<br> 翻訳結果を JSON/TXT 形式でローカルに保存。
    - **音声録音の紐付け**:<br> テキストだけでなく、録音データも同時に保存し、履歴からいつでも再生可能。
    - **削除機能**: <br>不要になったデータをサイドバーから簡単に削除可能。

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
1. **リポジトリをクローン**<br>
   推奨環境: Python 3.9 以上
    ```bash
   git clone https://github.com/linlin888-666/AI-Meeting-Assistant.git
   cd Meeting_AI

2. **仮想環境の作成と有効化**<br>
**Windows**
    ```bash
   python -m venv venv
   .\venv\Scripts\activate

<br>

   **Mac/Linux** 
    ```bash
   python3 -m venv venv
   source venv/bin/activate


3. **依存パッケージのインストール**
    ```bash
   pip install --upgrade pip<br>
   pip install -r requirements.txt

4. **環境変数の設定**<br>
   ルートディレクトリに .env ファイルを作成し、APIキーを設定してください。
    ```bash
   OPENAI_API_KEY=あなたのAPIキー

5. **アプリの起動**
    ```bash
   streamlit run app.py
## システムアーキテクチャ（System Architecture）
![System_Architecture](`docs`/System_Architecture.png)

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

## 🚀 今後のアップデート予定 (Roadmap)

### 現在、MVP（最小機能版）として動作していますが、さらなるユーザー体験向上のため、以下の機能を実装予定です：

1. **WebSocketによるリアルタイム処理の最適化**

- 現在のHTTPリクエスト方式からWebSocketへ移行し、音声認識の遅延（Latency）をさらに短縮します。

2. **重複翻訳の防止ロジックの改善**

- 音声の切り出しアルゴリズムを改良し、同じ文章が繰り返し翻訳される問題を解決します。

3. **UI/UXのブラッシュアップ**

- 翻訳結果の表示アニメーションを追加し、より直感的なフィードバックを提供します。

