import streamlit as st
from openai import OpenAI
from typing import cast
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam
st.set_page_config(layout="wide", page_title="ChatGPT-like clone")
st.title("ChatGPT-like clone")

# loading css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    css_class = "user-message" if role == "user" else "assistant-message"
    st.markdown(f"<div class='{css_class}'>{content}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("How can I help you today ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

    messages = [
        cast(ChatCompletionUserMessageParam | ChatCompletionAssistantMessageParam, m)
        for m in st.session_state.messages
    ]
    full_response = ""
    with st.chat_message("assistant"):  # <-- garde l'avatar ici
        response_container = st.empty()
        for chunk in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=messages,
                stream=True,
        ):
            content = chunk.choices[0].delta.content or ""
            full_response += content
            # on met à jour la div dans la boucle, toujours dans le chat_message
            response_container.markdown(
                f"<div class='assistant-message message-bubble'>{full_response}</div>",
                unsafe_allow_html=True
            )

    st.session_state.messages.append({"role": "assistant", "content": full_response})
