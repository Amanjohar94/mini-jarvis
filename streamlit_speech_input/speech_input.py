import os
import streamlit.components.v1 as components

_component_func = components.declare_component(
    "speech_input",
    path=os.path.join(os.path.dirname(__file__), "frontend")
)

def st_speech_input(label="🎙️ Speak", key=None):
    return _component_func(label=label, key=key, default="")
