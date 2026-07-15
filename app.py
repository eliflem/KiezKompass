import json
from pathlib import Path
from typing import Any

import streamlit as st

from src.llm import get_kiez_compass_response


with (Path(__file__).parent / "data" / "neighborhoods.json").open() as data_file:
    neighborhoods = json.load(data_file)


st.title("Kiez Compass")
st.caption("Tell us what matters to you in a Berlin neighborhood.")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "clarifying_rounds_used" not in st.session_state:
    st.session_state.clarifying_rounds_used = 0


def render_recommendation_cards(recommendations: list[dict[str, Any]]) -> None:
    for recommendation in recommendations:
        with st.container(border=True):
            st.markdown(f"**{recommendation['district']}**")
            st.caption(f"ZIP code: {recommendation['zip_code']}")
            st.write(recommendation["reason"])


def render_message(message: dict[str, Any]) -> None:
    with st.chat_message(message["role"]):
        content = message["content"]
        if (
            message["role"] == "assistant"
            and isinstance(content, dict)
            and content.get("action") == "recommend"
        ):
            render_recommendation_cards(content["recommendations"])
        else:
            st.write(content)


for message in st.session_state.messages:
    render_message(message)

if prompt := st.chat_input("Describe your ideal Kiez"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    current_round = min(st.session_state.clarifying_rounds_used + 1, 3)

    try:
        with st.spinner("Thinking with Gemini..."):
            response = get_kiez_compass_response(
                st.session_state.messages,
                current_round,
            )
    except Exception as error:
        st.error(f"Gemini request failed: {error}")
    else:
        if response["action"] == "clarify":
            st.session_state.clarifying_rounds_used = current_round
            st.session_state.messages.append(
                {"role": "assistant", "content": response["question"]}
            )
            with st.chat_message("assistant"):
                st.write(response["question"])
        else:
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                render_recommendation_cards(response["recommendations"])
