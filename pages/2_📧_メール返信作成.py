import streamlit as st

from core.gemini_client import generate_text_stream
from core.ui import render_page_header, render_result, render_sidebar

st.set_page_config(page_title="メール返信作成", page_icon="📧", layout="wide")
render_sidebar()
render_page_header("📧 メール返信作成", "受信したメールと伝えたい要点から、返信文を生成します。")

original_email = st.text_area("受信したメール本文", height=200, placeholder="返信したいメールの本文を貼り付けてください")
key_points = st.text_area("返信で伝えたい要点", height=120, placeholder="例: 提案内容は承諾するが、納期を1週間延ばしてほしい")

col1, col2, col3 = st.columns(3)
with col1:
    tone = st.selectbox("トーン", ["フォーマル・ビジネス", "丁寧だが柔らかい", "カジュアル・social"])
with col2:
    language = st.selectbox("言語", ["日本語", "英語"])
with col3:
    include_signature = st.checkbox("結びの挨拶・署名欄を含める", value=True)

if st.button("返信文を生成", type="primary", disabled=not key_points):
    system_instruction = "あなたはビジネスメールの返信作成に長けたアシスタントです。相手に失礼のない、自然な文面を作成してください。"
    prompt = f"""以下の情報をもとにメールの返信文を作成してください。

受信したメール本文:
{original_email or "（受信メール本文は提供されていません）"}

返信で伝えたい要点:
{key_points}

トーン: {tone}
言語: {language}
署名欄: {"文末に「署名欄」のプレースホルダーを含める" if include_signature else "含めない"}

返信メールの本文のみを出力してください。件名や説明は不要です。"""

    with st.container(border=True):
        result = st.write_stream(generate_text_stream(prompt, system_instruction))
    render_result(result, "email_reply.txt")
