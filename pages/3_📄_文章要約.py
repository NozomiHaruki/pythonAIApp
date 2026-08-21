import streamlit as st

from core.gemini_client import generate_text_stream
from core.ui import render_page_header, render_result, render_sidebar

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")
render_sidebar()
render_page_header("📄 文章要約", "長い文章を、指定した長さ・形式で要約します。")

source_text = st.text_area("要約したい文章", height=280, placeholder="ここに要約したい文章を貼り付けてください")

col1, col2 = st.columns(2)
with col1:
    summary_length = st.radio("要約の長さ", ["一言で（1文）", "短め（3行程度）", "標準（5〜7行）", "詳細（元の1/3程度）"], horizontal=False)
with col2:
    summary_format = st.radio("形式", ["箇条書き", "通常の文章"], horizontal=False)

if st.button("要約する", type="primary", disabled=not source_text):
    system_instruction = "あなたは文章を正確かつ簡潔に要約するアシスタントです。原文にない情報を付け加えないでください。"
    prompt = f"""以下の文章を要約してください。

要約の長さ: {summary_length}
出力形式: {summary_format}

--- 元の文章 ---
{source_text}
--- ここまで ---

要約結果のみを出力してください。"""

    with st.container(border=True):
        result = st.write_stream(generate_text_stream(prompt, system_instruction))
    render_result(result, "summary.txt")
