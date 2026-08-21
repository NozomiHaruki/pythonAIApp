"""Gemini API とのやり取りをまとめた薄いラッパー。"""

import streamlit as st
from google import genai
from google.genai import types


def get_client() -> genai.Client:
    api_key = st.session_state.get("api_key")
    if not api_key:
        st.error("サイドバーで Gemini APIキーを入力してください。")
        st.stop()
    return genai.Client(api_key=api_key)


def list_available_models(api_key: str) -> list[str]:
    """この API キーで実際に generateContent が使えるモデルIDの一覧を取得する。

    Gemini のモデルIDは提供終了・世代交代が頻繁にあるため、ハードコードせず
    API から都度取得する。取得できない場合は空リストを返す（呼び出し側でフォールバック）。
    """
    if not api_key:
        return []
    try:
        client = genai.Client(api_key=api_key)
        names = []
        for m in client.models.list():
            actions = getattr(m, "supported_actions", None) or []
            if "generateContent" not in actions:
                continue
            name = (m.name or "").removeprefix("models/")
            if name:
                names.append(name)
        return sorted(set(names))
    except Exception:
        return []


def generate_text(prompt: str, system_instruction: str | None = None) -> str:
    """プロンプトを送信し、完成したテキストを一括で返す。"""
    client = get_client()
    config = types.GenerateContentConfig(
        temperature=st.session_state.get("temperature", 0.7),
        system_instruction=system_instruction,
    )
    try:
        response = client.models.generate_content(
            model=st.session_state.get("model", "gemini-3.6-flash"),
            contents=prompt,
            config=config,
        )
        return response.text or ""
    except Exception as e:
        st.error(f"Gemini API の呼び出し中にエラーが発生しました: {e}")
        st.stop()


def generate_text_stream(prompt: str, system_instruction: str | None = None):
    """st.write_stream にそのまま渡せるジェネレータでテキストを逐次返す。"""
    client = get_client()
    config = types.GenerateContentConfig(
        temperature=st.session_state.get("temperature", 0.7),
        system_instruction=system_instruction,
    )
    try:
        for chunk in client.models.generate_content_stream(
            model=st.session_state.get("model", "gemini-3.6-flash"),
            contents=prompt,
            config=config,
        ):
            if chunk.text:
                yield chunk.text
    except Exception as e:
        st.error(f"Gemini API の呼び出し中にエラーが発生しました: {e}")
        st.stop()
