import streamlit as st

from core.gemini_client import generate_text_stream
from core.ui import render_page_header, render_result, render_sidebar

st.set_page_config(page_title="校正・リライト", page_icon="✨", layout="wide")
render_sidebar()
render_page_header("✨ 校正・リライト", "誤字脱字のチェックや、文体・トーンの変更を行います。")

source_text = st.text_area("元の文章", height=280, placeholder="ここに校正・リライトしたい文章を貼り付けてください")

purpose = st.selectbox(
    "目的",
    [
        "誤字脱字・文法チェックのみ（内容や文体は変えない）",
        "より丁寧な文章にする",
        "より簡潔にする",
        "よりカジュアルにする",
        "よりフォーマル・ビジネス向けにする",
        "より説得力のある文章にする",
    ],
)
extra = st.text_area("追加の指示（任意）", placeholder="例: 語尾は「です・ます調」に統一してほしい")

if st.button("実行する", type="primary", disabled=not source_text):
    system_instruction = "あなたは日本語の文章校正・編集のプロです。原文の意味や主張を保ったまま、指示に沿って文章を改善してください。"
    prompt = f"""以下の文章を、指定された目的に沿って校正・リライトしてください。

目的: {purpose}
追加の指示: {extra or "特になし"}

--- 元の文章 ---
{source_text}
--- ここまで ---

リライト後の文章のみを出力してください。説明や前置きは不要です。"""

    with st.container(border=True):
        result = st.write_stream(generate_text_stream(prompt, system_instruction))
    render_result(result, "revised_text.txt")
