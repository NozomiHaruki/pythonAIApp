import streamlit as st

from core.gemini_client import generate_text_stream
from core.ui import render_page_header, render_result, render_sidebar

st.set_page_config(page_title="翻訳", page_icon="🌐", layout="wide")
render_sidebar()
render_page_header("🌐 翻訳", "自然な訳文への翻訳を行います。")

source_text = st.text_area("原文", height=250, placeholder="翻訳したい文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    target_language = st.selectbox(
        "翻訳先言語", ["英語", "日本語", "中国語（簡体字）", "中国語（繁体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語"]
    )
with col2:
    style = st.selectbox("文体", ["自然な意訳（読みやすさ重視）", "原文に忠実な直訳", "ビジネス文書調", "カジュアル・口語調"])

if st.button("翻訳する", type="primary", disabled=not source_text):
    system_instruction = "あなたはプロの翻訳者です。ニュアンスを正確に保ちながら、自然な訳文を作成してください。"
    prompt = f"""以下の文章を{target_language}に翻訳してください。

文体: {style}

--- 原文 ---
{source_text}
--- ここまで ---

翻訳結果のみを出力してください。"""

    with st.container(border=True):
        result = st.write_stream(generate_text_stream(prompt, system_instruction))
    render_result(result, "translation.txt")
