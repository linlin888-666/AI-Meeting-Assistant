import streamlit as st
import datetime
import time
import os
import io

def show_upload():
    if "temp_uploaded_file" not in st.session_state:
        st.session_state.temp_uploaded_file = None
    # --- 1. ステートの初期化 ---
    if "temp_transcript" not in st.session_state:
        st.session_state.temp_transcript = []
    if "show_dialog" not in st.session_state:
        st.session_state.show_dialog = None 

    # --- 2. ヘッダー：戻るボタンと言語選択 ---
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬅️ 戻る"):
            st.session_state.show_dialog = "exit"
    
    with col2:
        target_lang = st.selectbox(
            "翻訳ターゲット言語", 
            ["翻訳なし", "中国語", "英語", "日本語"],
            label_visibility="collapsed"
        )

    # --- 3. ダイアログ制御 (保存・終了) ---
    if st.session_state.show_dialog == "exit":
        with st.container(border=True):
            st.warning("終了する前に内容を保存しますか？")
            c1, c2, c3 = st.columns(3)
            if c1.button("保存して戻る", type="primary"):
                st.session_state.show_dialog = "save"
                st.rerun()
            if c2.button("保存せずに戻る"):
                st.session_state.temp_transcript = []
                st.session_state.page = "main"
                st.session_state.show_dialog = None
                st.rerun()
            if c3.button("キャンセル"):
                st.session_state.show_dialog = None
                st.rerun()

    if st.session_state.show_dialog == "save":
        with st.container(border=True):
            st.subheader("💾 ファイル保存")
            title = st.text_input("ファイル名を入力してください", 
                                value=f"録音データ_{datetime.datetime.now().strftime('%m%d_%H%M')}")
            if st.button("確定して保存"):
                save_dir = "saved_records"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                    
                try:
                    # 1. .txt 人間読めるフォイル
                    save_content = f"タイトル: {title}\n"
                    save_content += f"作成日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    save_content += "-"*30 + "\n"
                    for item in st.session_state.temp_transcript:
                        save_content += f"[{item['time']}] 原文: {item['text']}\n"
                        if item.get('trans'):
                            save_content += f"       翻訳: {item['trans']}\n"
                        save_content += "\n"
                        
                    with open(os.path.join(save_dir, f"{title}.txt"), "w", encoding="utf-8") as f:
                        f.write(save_content)
                    
                    # 2. .json データ
                    import json
                    with open(os.path.join(save_dir, f"{title}.json"), "w", encoding="utf-8") as f:
                        json.dump(st.session_state.temp_transcript, f, ensure_ascii=False, indent=2)
                    
                    # 3. 更新と保存
                    st.session_state.saved_files[title] = st.session_state.temp_transcript
                    st.success(f"✅ 保存完了: {title}")
                    time.sleep(1)
                    
                    # リセット状态
                    st.session_state.temp_transcript = []
                    st.session_state.page = "main"
                    st.session_state.show_dialog = None
                    st.rerun()
                except Exception as e:
                    st.error(f"保存エラー: {e}")

    # --- 4. アップロードエリア ---
    st.title("📂 ファイルアップロード翻訳")
    uploaded_file = st.file_uploader("音声または動画ファイルを選択 (mp3, mp4, wav, avi,m4a)", type=["mp3", "mp4", "wav", "avi","m4a"])

    if uploaded_file:
        # アップロードのデータを session_stateに入れる，データを守る
        st.session_state.temp_uploaded_file = uploaded_file
        if st.button("解析を開始する", use_container_width=True):
            with st.spinner("AIが解析中です..."):
                handler = st.session_state.ai_handler
                # AI処理を実行 (target_langが"翻訳なし"以外なら翻訳ON)
                results = handler.process_audio_object(
                    uploaded_file, 
                    target_lang, 
                    (target_lang != "翻訳なし"), 
                    datetime.datetime.now()
                )
                if results:
                    st.session_state.temp_transcript = results
                    st.rerun()

    # --- 5. テキスト表示エリア ---
    st.markdown("### 📄 解析結果")
    # CSSで薄いグレーの枠線を再現
    st.markdown("""
        <style>
        .text-box {
            border: 1px solid #d3d3d3;
            border-radius: 5px;
            padding: 15px;
            background-color: #f9f9f9;
            min-height: 300px;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        if not st.session_state.temp_transcript:
            st.info("ファイルを選択して「解析を開始」ボタンを押してください。")
        else:
            for item in st.session_state.temp_transcript:
                st.markdown(f"**[{item['time']}]**")
                st.write(f"原文: {item['text']}")
                if item.get('trans'):
                    st.markdown(f"<span style='color:#28a745'>翻訳: {item['trans']}</span>", unsafe_allow_html=True)
                st.markdown("---")

    # --- 6. 下部保存ボタン ---
    if st.session_state.temp_transcript:
        if st.button("💾 この内容を保存する", use_container_width=True):
            st.session_state.show_dialog = "save"
            st.rerun()