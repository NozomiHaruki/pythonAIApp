"""各ページで共通利用する UI パーツ。"""

import os

import streamlit as st
from dotenv import load_dotenv

from core.gemini_client import list_available_models

load_dotenv()

MANUAL_ENTRY = "その他（手動入力）"

# API からモデル一覧を取得できなかった場合のみ使うフォールバック。
FALLBACK_MODEL_OPTIONS = [
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    MANUAL_ENTRY,
]


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_model_list(api_key: str) -> list[str]:
    return list_available_models(api_key)


def render_sidebar() -> None:
    """APIキー・モデル・temperature の設定をサイドバーに表示する。"""
    st.sidebar.title("⚙️ 設定")

    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")
    st.session_state.api_key = st.sidebar.text_input(
        "Gemini API キー",
        value=st.session_state.api_key,
        type="password",
        help="環境変数 GEMINI_API_KEY (.env) からも読み込めます。",
    )

    fetched_models = _cached_model_list(st.session_state.api_key) if st.session_state.api_key else []
    model_options = (fetched_models if fetched_models else FALLBACK_MODEL_OPTIONS[:-1]) + [MANUAL_ENTRY]
    if not fetched_models:
        st.sidebar.caption("⚠️ モデル一覧を取得できなかったため候補を固定表示中です。古いモデルはエラーになる場合があります。")

    default_model = st.session_state.get("model", model_options[0])
    index = model_options.index(default_model) if default_model in model_options else len(model_options) - 1
    selected = st.sidebar.selectbox("モデル", model_options, index=index)
    if selected == MANUAL_ENTRY:
        st.session_state.model = st.sidebar.text_input(
            "モデルIDを入力", value=st.session_state.get("model", "")
        )
    else:
        st.session_state.model = selected

    st.session_state.temperature = st.sidebar.slider(
        "創造性 (temperature)", 0.0, 1.0, st.session_state.get("temperature", 0.7), 0.05
    )

    st.sidebar.divider()
    st.sidebar.caption("個人用 AI ライティングツール ✍️")


def render_page_header(title: str, description: str) -> None:
    st.title(title)
    st.caption(description)
    st.divider()


def render_result(text: str, filename: str) -> None:
    """生成結果をコピーしやすい形式で表示し、ダウンロードボタンも出す。"""
    st.text_area("生成結果", value=text, height=320)
    st.download_button(
        "テキストファイルとして保存",
        data=text,
        file_name=filename,
        mime="text/plain",
    )
