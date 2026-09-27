from pathlib import Path
import os
import subprocess
import sys

import streamlit as st

def load_streamlit_secrets():
    try:
        if "GROQ_API_KEY" in st.secrets:
            os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
        if "MODEL_NAME" in st.secrets:
            os.environ["MODEL_NAME"] = st.secrets["MODEL_NAME"]
    except Exception:
        pass

load_streamlit_secrets()

from src.config import DATABASE_PATH
from src.graph import ask_agent

def ensure_database():
    if DATABASE_PATH.exists():
        return

    script = Path(__file__).resolve().parent / "scripts" / "seed_db.py"
    subprocess.run(
        [sys.executable, str(script)],
        check=True,
    )

ensure_database()

st.set_page_config(
    page_title="Enterprise AI Operations Agent",
    page_icon="🤖",
    layout="wide",
)

st.title("Enterprise AI Operations Agent")
st.caption(
    "LangGraph + Tool Calling + RAG + SQL + MCP + Human Approval"
)

with st.sidebar:
    st.subheader("Demo IDs")
    st.code("Customer: CUST-002\nOrder: ORD-1002")
    st.markdown(
        """
        **Try these**
        - Why is order ORD-1002 delayed?
        - What is the refund policy for delayed orders?
        - Show support history for CUST-002.
        - Create a support ticket for CUST-002 about ORD-1002.
        """
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask about customers, orders, tickets, or policies...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Agent is working..."):
            try:
                answer = ask_agent(question)
            except Exception as exc:
                answer = f"Error: {exc}"

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
    })
