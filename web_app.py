# app/web_app.py

import streamlit as st

from core import get_client, chat_with_memory     # CORRIGIDO
from subjects import detect_subject               # CORRIGIDO

def apply_theme(theme):
    themes = {
        "Green Academic": {
            "background": "#0C1B0C",
            "secondary": "#112A11",
            "text": "white",
            "primary": "#2ECC71",
        },
        "Dark Purple": {
            "background": "#0A0F24",
            "secondary": "#11182F",
            "text": "white",
            "primary": "#6C63FF",
        },
        "Neon Tech": {
            "background": "#000000",
            "secondary": "#0A0A0A",
            "text": "#FFFFFF",
            "primary": "#39FF14",
        },
        "Math Chalkboard": {
            "background": "#0F1F0F",      # Verde quadro-negro
            "secondary": "#1A351A",      # Verde giz mais claro
            "text": "#F8F8F2",           # Branco levemente amarelado (giz)
            "primary": "#88FF88",        # Verde giz para botões
        },
    }

    t = themes[theme]

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {t['background']} !important;
            color: {t['text']} !important;
        }}
        .stSidebar {{
            background-color: {t['secondary']} !important;
        }}
        h1, h2, h3, h4, h5, h6, p, span {{
            color: {t['text']} !important;
        }}
        .stButton>button {{
            background-color: {t['primary']} !important;
            color: black !important;
            border-radius: 6px;
            padding: 0.6rem 1rem;
            border: none;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def init_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "client" not in st.session_state:
        st.session_state.client = get_client()


def main():
    st.set_page_config(
        page_title="Tutor de Matemática e Física",
        page_icon="📘",
    )

    init_session_state()

    st.title("📘 Tutor de Matemática com IA")
    st.markdown(
        "Faça perguntas de Matemática. "
        "O tutor responde passo a passo, com foco em entendimento conceitual."
    )

    with st.sidebar:
        theme_choice = st.selectbox(
            "Tema visual",
            ["Green Academic", "Dark Purple", "Neon Tech", "Math Chalkboard"],
            index=0
        )

        apply_theme(theme_choice)

        st.header("Configurações")
        max_history = st.slider(
            "Tamanho da memória (número de mensagens anteriores)",
            min_value=2,
            max_value=30,
            value=10,
        )
        if st.button("Limpar conversa"):
            st.session_state.history = []
            st.success("Histórico limpo.")

    # Mostrar histórico
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_message = st.chat_input("Digite sua pergunta de Matemática ou Física...")

    if user_message:
        with st.chat_message("user"):
            st.markdown(user_message)

        reply, new_history = chat_with_memory(
            client=st.session_state.client,
            history=st.session_state.history,
            user_message=user_message,
            max_history=max_history,
            source="web",
        )

        st.session_state.history = new_history

        with st.chat_message("assistant"):
            st.markdown(reply)


if __name__ == "__main__":
    main()
