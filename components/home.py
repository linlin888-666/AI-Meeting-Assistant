import streamlit as st
def show_home():
    st.title("AI会議議事録システム")
    st.write("モードを選択してください：")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        with st.container(border=True):
            st.subheader("🎙️ リアルタイム翻訳・録音")
            st.write("マイクを使用して、リアルタイムで会議を記録および翻訳します。")
            if st.button("リアルタイムモードを開始", use_container_width=True):
                st.session_state.page = "live"
                st.rerun()
                
    with col_right:
        with st.container(border=True):
            st.subheader("📁 ファイルアップロード")
            st.write("録音済みの音声ファイル（MP3/WAV等）をアップロードして解析します。")
            if st.button("アップロードモードを開始", use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()
    
    with st.sidebar:
        st.title("📚 保存済み内容")
        if "saved_files" not in st.session_state or not st.session_state.saved_files:
            st.write("保存されたデータはありません。")
        else:
            for title in st.session_state.saved_files.keys():
                if st.button(f"📄 {title}", use_container_width=True):
                    # 这里可以写点击历史文件后跳转详情的逻辑
                    st.info(f"「{title}」を表示します（実装中）")