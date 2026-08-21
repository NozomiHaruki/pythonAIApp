import streamlit as st

from core.gemini_client import generate_text_stream
from core.ui import render_page_header, render_result, render_sidebar

st.set_page_config(page_title="タイトル・キャッチコピー生成", page_icon="💡", layout="wide")
render_sidebar()
render_page_header("💡 タイトル・キャッチコピー生成", "内容の説明から、タイトルやキャッチコピーを複数案生成します。")

description = st.text_area("内容の説明・要約", height=150, placeholder="例: リモートワーカー向けの時間管理術を紹介する記事")

col1, col2 = st.columns(2)
with col1:
    purpose = st.selectbox(
        "用途",
        ["ブログ記事タイトル", "広告キャッチコピー", "YouTube動画タイトル", "商品・サービス名", "プレスリリース見出し"],
    )
with col2:
    num_ideas = st.slider("生成する案数", 3, 10, 5)

style_hint = st.text_input("スタイルの希望（任意）", placeholder="例: 数字を入れて具体性を出したい、疑問形にしたい など")

if st.button("生成する", type="primary", disabled=not description):
    system_instruction = "あなたはキャッチコピーやタイトル制作を専門とするコピーライターです。クリックしたくなる、印象に残る案を作成してください。"
    prompt = f"""以下の内容について、{purpose}を{num_ideas}案考えてください。

内容の説明: {description}
スタイルの希望: {style_hint or "特になし"}

各案は番号付きリストで出力し、余計な説明は加えないでください。"""

    with st.container(border=True):
        result = st.write_stream(generate_text_stream(prompt, system_instruction))
    render_result(result, "titles.txt")
