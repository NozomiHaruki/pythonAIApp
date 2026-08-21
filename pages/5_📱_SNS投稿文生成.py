import streamlit as st

from core.gemini_client import generate_text_stream
from core.ui import render_page_header, render_result, render_sidebar

st.set_page_config(page_title="SNS投稿文生成", page_icon="📱", layout="wide")
render_sidebar()
render_page_header("📱 SNS投稿文生成", "媒体に合わせた投稿文を複数案生成します。")

content = st.text_area("投稿したい内容", height=150, placeholder="例: 新しく発売したハンドメイドアクセサリーの紹介")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("プラットフォーム", ["X (Twitter)", "Instagram", "Facebook", "LinkedIn", "Threads"])
    tone = st.selectbox("トーン", ["親しみやすい", "テンション高め・ワクワク感", "落ち着いた・信頼感重視", "ユーモラス"])
with col2:
    num_variations = st.slider("生成する案数", 1, 5, 3)
    use_hashtags = st.checkbox("ハッシュタグを含める", value=True)
    use_emoji = st.checkbox("絵文字を使う", value=True)

platform_limits = {
    "X (Twitter)": "140字程度に収める",
    "Instagram": "改行を活用し、読みやすいキャプション形式にする（長さの制約は緩め）",
    "Facebook": "やや長めでも良いので、背景や文脈を含めて書く",
    "LinkedIn": "ビジネス・専門性を意識したトーンにする",
    "Threads": "カジュアルで会話的な短文にする",
}

if st.button("投稿文を生成", type="primary", disabled=not content):
    system_instruction = "あなたはSNSマーケティングに精通したコピーライターです。プラットフォームの特性に合わせた投稿文を作成してください。"
    prompt = f"""以下の条件でSNS投稿文を{num_variations}案作成してください。

投稿したい内容: {content}
プラットフォーム: {platform}（{platform_limits[platform]}）
トーン: {tone}
ハッシュタグ: {"投稿の最後に関連性の高いものを3〜5個含める" if use_hashtags else "含めない"}
絵文字: {"適度に使う" if use_emoji else "使わない"}

各案は「案1」「案2」のように番号を付けて、それぞれ改行で区切って出力してください。"""

    with st.container(border=True):
        result = st.write_stream(generate_text_stream(prompt, system_instruction))
    render_result(result, "sns_posts.txt")
