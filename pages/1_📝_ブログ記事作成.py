import streamlit as st

from core.gemini_client import generate_text_stream
from core.ui import render_page_header, render_result, render_sidebar

st.set_page_config(page_title="ブログ記事作成", page_icon="📝", layout="wide")
render_sidebar()
render_page_header("📝 ブログ記事作成", "テーマや読者を指定して、ブログ記事の下書きを生成します。")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("テーマ・トピック", placeholder="例: 在宅ワークの生産性を上げる習慣")
    audience = st.text_input("想定読者", placeholder="例: 20〜30代の在宅ワーカー")
    keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）", placeholder="例: 時間管理, 集中力, ルーティン")
with col2:
    length = st.select_slider(
        "文字数の目安", options=["短め (300字)", "標準 (800字)", "長め (1500字)", "詳細 (3000字)"], value="標準 (800字)"
    )
    tone = st.selectbox("トーン", ["丁寧・解説調", "カジュアル・親しみやすい", "専門的・信頼性重視", "エモーショナル・共感重視"])
    include_headings = st.checkbox("見出し構成（H2/H3）を含める", value=True)

extra = st.text_area("追加の指示（任意）", placeholder="例: 体験談を交えて書いてほしい、結論を先に書いてほしい など")

if st.button("記事を生成", type="primary", disabled=not topic):
    system_instruction = "あなたは日本語のプロのブログライター兼SEOエディターです。読みやすく、読者の役に立つ記事を書いてください。"
    prompt = f"""以下の条件でブログ記事を書いてください。

テーマ: {topic}
想定読者: {audience or "特に指定なし"}
含めたいキーワード: {keywords or "特に指定なし"}
文字数の目安: {length}
トーン: {tone}
見出し構成: {"Markdown の見出し（##, ###）を使って構成すること" if include_headings else "見出しは使わず、通し文章で書くこと"}
追加の指示: {extra or "特になし"}

記事本文のみを出力してください。前置きや説明文は不要です。"""

    with st.container(border=True):
        result = st.write_stream(generate_text_stream(prompt, system_instruction))
    render_result(result, "blog_post.txt")
