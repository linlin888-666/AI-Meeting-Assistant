import os
import streamlit as st
from openai import OpenAI
import datetime

class AIHandler:
    """
    OpenAI APIとの通信を担当するクラス
    """
    def __init__(self, api_key):
        # クライアントの初期化 (初始化客户端)
        self.client = OpenAI(api_key=api_key)

    def process_audio(self, audio_file_path, target_lang, trans_on):
        """
        音声をテキスト化し、必要に応じて翻訳する
        """
        try:
            # 1. Whisper APIで文字起こし
            with open(audio_file_path, "rb") as f:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=f,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            processed_segments = []

            # 2. 各セグメントの処理 
            for seg in response.segments:
                start_sec = int(seg['start'])
                # 時間フォーマット [mm:ss] 
                time_stamp = f"{start_sec//60:02d}:{start_sec%60:02d}"
                original_text = seg['text']
                translation = ""

                # 3. 翻訳が必要な場合、GPTで翻訳 
                if trans_on and target_lang != "翻訳なし":
                    translation = self.translate_text(original_text, target_lang)

                processed_segments.append({
                    "time": time_stamp,
                    "text": original_text,
                    "trans": translation
                })

            return processed_segments

        except Exception as e:
            # エラー処理 
            print(f"AI処理エラー: {e}")
            return None

    def translate_text(self, text, target_lang):
        """
        GPT-4o-miniを使用してテキストを翻訳する
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"あなたは優秀な通訳者です。以下の文章を{target_lang}に翻訳してください。"},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content

    def process_audio_object(self, audio_file, target_lang, trans_on, start_time):
        try:
            response = self.client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["segment"]
            )

            # 始める時間
            import datetime
            now = datetime.datetime.now()
            # 何秒進める
            elapsed = int((now - start_time).total_seconds())

            new_results = []
            for seg in response.segments:
                current_sec = elapsed + int(seg.start)
                time_stamp = f"{current_sec//60:02d}:{current_sec%60:02d}"
                
                text = seg.text
                trans = ""
                if trans_on and target_lang != "翻訳なし":
                    trans = self.translate_text(text, target_lang)
                
                new_results.append({
                    "time": time_stamp,
                    "text": text,
                    "trans": trans
                })
            return new_results
        except Exception as e:
            st.error(f"AI Handler Error: {e}")
            return None