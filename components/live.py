import streamlit as st
import datetime
import time
import os
import json
import io
from audio_recorder_streamlit import audio_recorder

def show_live():
    # --- 1. ステートの初期化 ---
    if "transcript_history" not in st.session_state:
        st.session_state.transcript_history = []
    if "full_audio" not in st.session_state:
            st.session_state.full_audio = b"" 
    if "start_time" not in st.session_state:
            st.session_state.start_time = None
    if "last_processed_text" not in st.session_state:
        st.session_state.last_processed_text = ""
    if "show_dialog" not in st.session_state:
        st.session_state.show_dialog = None

    # --- 2. 戻るボタン (左上) ---
    col_back, col_title = st.columns([1, 8])
    with col_back:
        if st.button("⬅️ 戻る"):
            st.session_state.show_dialog = "exit"

    # --- 3. ダイアログ制御 (保存・終了) ---
    if st.session_state.show_dialog == "exit":
        with st.container(border=True):
            st.warning("終了する前に内容を保存しますか？")
            c1, c2, c3 = st.columns(3)
            if c1.button("保存して戻る", type="primary"):
                st.session_state.show_dialog = "save"
                st.rerun()
            if c2.button("保存せずに戻る"):
                # 破棄してメインへ
                st.session_state.transcript_history = []
                st.session_state.start_time = None
                st.session_state.page = "main"
                st.session_state.show_dialog = None
                st.rerun()
            if c3.button("キャンセル"):
                st.session_state.show_dialog = None
                st.rerun()

    if st.session_state.show_dialog == "save":
        with st.container(border=True):
            st.subheader("💾 ファイル保存")
            title = st.text_input("ファイル名を入力してください", value=f"リアルタイム録音_{datetime.datetime.now().strftime('%m%d_%H%M')}")
            # --- 保存ボタンについて---
            if st.button("保存を確定"):
                save_dir = "saved_records"
                if not os.path.exists(save_dir): os.makedirs(save_dir)
                
                try:
                    # 🌟 音声とデータの保存
                    timestamp = datetime.datetime.now().strftime('%m%d_%H%M%S')
                    audio_path = os.path.join(save_dir, f"{title}_{timestamp}.wav")
                    
                    with open(audio_path, "wb") as f:
                        f.write(st.session_state.full_audio)
                    
                    record_to_save = {
                        "transcript": st.session_state.transcript_history,
                        "audio_path": audio_path
                    }
                    
                    with open(os.path.join(save_dir, f"{title}.json"), "w", encoding="utf-8") as f:
                        json.dump(record_to_save, f, ensure_ascii=False, indent=2)
                    
                    st.success("保存完了！")
                    time.sleep(1)
                    # 状態リセット
                    st.session_state.full_audio = b""
                    st.session_state.transcript_history = []
                    st.session_state.page = "main"
                    st.rerun()
                except Exception as e:
                    st.error(f"保存エラー: {e}")

    # --- 4. メイン画面 UI ---
    st.title("🎙️ リアルタイム会議録")
    st.caption(f"🗓️ 実施日: {datetime.datetime.now().strftime('%Y/%m/%d')}")

    # テキスト表示エリア
    display_area = st.container(height=400, border=True)
    with display_area:
        if not st.session_state.transcript_history:
            st.info("マイクボタンを押して話してください。4秒間の沈黙で自動解析されます。")
        else:
            for item in st.session_state.transcript_history:
                st.markdown(f"""
                **[{item['time']}]** {item['text']}  
                <div style="color: #28a745; font-size: 0.95em; margin-top: -5px; margin-bottom: 10px; padding-left: 15px; border-left: 2px solid #28a745;">
                ↳ 翻訳: {item.get('trans', '')}
                </div>
                """, unsafe_allow_html=True)

    # コントロールパネル
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        target_lang = st.selectbox("翻訳言語", ["中国語", "日本語", "英語"], label_visibility="collapsed")
    with c2:
        trans_on = st.toggle("自動翻訳", value=True)

    # 録音コンポーネント
    audio_bytes = audio_recorder(
        text="録音中 (4秒の沈黙で自動翻訳)",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_size="3x",
        pause_threshold=4.0, 
        key="live_recorder"
    )

    # AI 処理ロジック
    if audio_bytes:
        st.session_state.full_audio += audio_bytes
        if st.session_state.start_time is None:
            st.session_state.start_time = datetime.datetime.now()

        handler = st.session_state.ai_handler
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "recording.wav"
        
        with st.spinner("AI解析中..."):
            new_segments = handler.process_audio_object(
                audio_file, 
                target_lang, 
                trans_on, 
                st.session_state.start_time
            )
            
            if new_segments:
                for seg in new_segments:
                    current_text = seg['text'].strip()
                    # 重複チェック
                    if current_text and current_text != st.session_state.last_processed_text:
                        st.session_state.transcript_history.append(seg)
                        st.session_state.last_processed_text = current_text
                
                # 自動更新
                st.rerun()

    # 下部の手動保存ボタン (録音データがある場合のみ表示)
    if st.session_state.transcript_history:
        st.divider()
        if st.button("💾 この内容を保存する", use_container_width=True):
            st.session_state.show_dialog = "save"
            st.rerun()