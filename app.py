import streamlit as st
import os
import json
import datetime
import time
from dotenv import load_dotenv

from styles import apply_custom_css
from components.home import show_home
from components.live import show_live
from components.upload import show_upload
from utils.ai_handler import AIHandler

# --- 環境設定と初期化 ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ページ基本設定 
st.set_page_config(layout="wide", page_title="AI会議議事録アシスタント")
if "saved_files" not in st.session_state:
    st.session_state.saved_files = {}
    save_dir = "saved_records"
    if os.path.exists(save_dir):
        for file_name in os.listdir(save_dir):
            if file_name.endswith(".json"):
                title = file_name.replace(".json", "")
                try:
                    with open(os.path.join(save_dir, file_name), "r", encoding="utf-8") as f:
                        # 这样读取出的数据里就带着 audio_path 了
                        st.session_state.saved_files[title] = json.load(f)
                except:
                    pass

if "start_time" not in st.session_state:
    st.session_state.start_time = None 
# --- 3. セッション状態の初期化 ---
if "page" not in st.session_state:
    st.session_state.page = "main"

if "transcript_history" not in st.session_state:
    st.session_state.transcript_history = []

# AIハンドラー（頭脳）をセッションに保存して使い回す
if "ai_handler" not in st.session_state:
    if api_key:
        st.session_state.ai_handler = AIHandler(api_key)
    else:
        st.error("API Keyが見つかりません。.envファイルを確認してください。")
        st.stop()


# --- sidebar歴史管理 ---
with st.sidebar:
    st.title("📚 履歴管理")
    st.markdown("---")
    
    if not st.session_state.saved_files:
        st.caption("保存済みのデータはありません。")
    else:
        # list() を使うことで削除時のエラーを防ぐ
        for title in list(st.session_state.saved_files.keys()):
            col_file, col_del = st.columns([4, 1])
            
            with col_file:
                #  keyを sidebar_ にすることで重複エラー(DuplicateElementId)を回避
                if st.button(f"📄 {title}", key=f"sidebar_btn_{title}", use_container_width=True):
                    st.session_state.selected_title = title
                    st.session_state.page = "history_detail"
                    st.rerun()
            
            with col_del:
                # 二次確認ポップオーバー
                with st.popover("🗑️"):
                    st.write("このファイルを削除しますか？")
                    if st.button("確定", key=f"del_confirm_{title}", type="primary", use_container_width=True):
                        try:
                            save_dir = "saved_records"
                            data = st.session_state.saved_files[title]
                            
                            # 古いリスト形式と新しい辞書形式の両方に対応
                            audio_path = data.get("audio_path") if isinstance(data, dict) else None
                            
                            # 1. ローカルファイルの削除
                            for ext in [".json", ".txt"]:
                                p = os.path.join(save_dir, f"{title}{ext}")
                                if os.path.exists(p): os.remove(p)
                            
                            if audio_path and os.path.exists(audio_path):
                                os.remove(audio_path)
                            
                            # 2. メモリから削除
                            del st.session_state.saved_files[title]
                            
                            # 3. 表示中のページならリセット
                            if st.session_state.get("selected_title") == title:
                                st.session_state.page = "main"
                            
                            st.toast(f"「{title}」を削除しました")
                            time.sleep(0.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"削除エラー: {e}")

# --- 4. UIの適用 (CSS) ---
apply_custom_css()

# --- 5. ルーティング ---
# メイン画面の表示
if st.session_state.page == "main":
    show_home()

# リアルタイム録音・翻訳画面の表示 
elif st.session_state.page == "live":
    show_live()

# アップロード画面（今後実装予定）
elif st.session_state.page == "upload":
    show_upload()

elif st.session_state.page == "history_detail":
    title = st.session_state.selected_title
    data = st.session_state.saved_files.get(title, {})
    
    if st.button("⬅️ 戻る"):
        st.session_state.page = "main"
        st.rerun()
        
    st.title(f"📄 {title}")
    
    # 音声プレイヤーの表示
    audio_path = data.get("audio_path") if isinstance(data, dict) else None
    if audio_path and os.path.exists(audio_path):
        st.audio(audio_path)
    
    # テキストの表示 (辞書から transcript を取得)
    with st.container(border=True):
        # dataが辞書なら .get()、リストならそのまま使う
        transcript = data.get("transcript", []) if isinstance(data, dict) else data
        
        for item in transcript:
            st.markdown(f"**[{item.get('time')}]**")
            st.write(f"原文: {item.get('text')}")
            if item.get('trans'):
                st.markdown(f"<span style='color:green'>翻訳: {item['trans']}</span>", unsafe_allow_html=True)
            st.divider()
    

    # プレビュー表示
    if "selected_record" in st.session_state:
        st.markdown("---")
        st.subheader(f"🔍 プレビュー: {st.session_state.selected_title}")
        for item in st.session_state.selected_record[:3]:  # 最新3件のみ表示
            st.caption(f"**{item['time']}** {item['text'][:30]}...")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("閉じる"):
                del st.session_state.selected_record
                st.rerun()
        with c2:
            pass