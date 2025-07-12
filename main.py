import streamlit as st
from st_chat_input_multimodal import multimodal_chat_input
from utils.config import FEATURES
from modules import chat, news, markets, tasks, weather, notes
import os
import streamlit.components.v1 as components

# ---------------- Voice Synth ----------------
voice_script = """
<script>
    function speak(text) {
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'en-US';
        msg.pitch = 1;
        msg.rate = 1;
        speechSynthesis.cancel();
        speechSynthesis.speak(msg);
    }
    window.addEventListener("DOMContentLoaded", () => {
        let text = new URLSearchParams(window.location.search).get("say");
        if (text) speak(decodeURIComponent(text));
    });
</script>
"""

def speak_browser(text: str):
    components.html(voice_script + f"""
        <script>
            if (!window.location.search.includes('say=')) {{
                const url = new URL(window.location.href);
                url.searchParams.set('say', encodeURIComponent({text!r}));
                window.location.href = url.toString();
            }}
        </script>
    """, height=0)

# ---------------- Page Config ----------------
st.set_page_config(page_title="Mini-JARVIS", layout="wide", initial_sidebar_state="expanded")
st.title("🤖 Mini-JARVIS — Your Local AI Assistant")

# ---------------- Session State ----------------
if "voice_enabled" not in st.session_state:
    st.session_state["voice_enabled"] = True

if "tools" not in st.session_state:
    st.session_state.tools = {
        "Weather": True,
        "News": True,
        "Tasks": True,      # ✅ Corrected
        "Markets": True
    }


# ---------------- Sidebar ----------------
with st.sidebar:
    st.subheader("🧰 Jarvis Tools")
    for tool in st.session_state.tools:
        st.session_state.tools[tool] = st.checkbox(tool, value=st.session_state.tools[tool])

    st.subheader("🔊 Voice Settings")
    st.session_state["voice_enabled"] = st.toggle("Enable Voice", value=True)
    st.selectbox("Select Voice", ["Default", "Male", "Female"], index=0)

# ---------------- Chat UI ----------------
if FEATURES.get("chat"):
    st.header("🧠 Chat with GPT")

    result = multimodal_chat_input(enable_voice_input=True, voice_language="en-US")

    if result:
        if "text" in result and result["text"]:
            spoken_text = result["text"]
            st.markdown(f"**🧑 You said:** {spoken_text}")
            response = chat.ask_gpt(spoken_text)
            st.markdown(f"**🤖 Jarvis:** {response}")
            if st.session_state["voice_enabled"]:
                if st.button("🔊 Play Jarvis Voice"):
                    speak_browser(response)
        elif "audioFile" in result:
            st.audio(result["audioFile"])

# ---------------- Weather ----------------
if FEATURES.get("weather") and st.session_state.tools.get("Weather"):
    st.header("🌤️ Weather")
    city = st.text_input("Enter city name", value="Delhi", key="weather_city")
    if st.button("Get Weather"):
        st.success(weather.get_weather(city))

# ---------------- News ----------------
if FEATURES.get("news") and st.session_state.tools.get("News"):
    st.header("📰 News Summary")
    for article in news.get_top_headlines():
        st.markdown(f"**{article['title']}**\n\n{article['description']}\n")

# ---------------- Markets ----------------
if FEATURES.get("markets") and st.session_state.tools.get("Markets"):
    st.header("📈 Market Tracker")
    st.line_chart(markets.get_stock_data("AAPL"))

# ---------------- Notes/Tasks ----------------
if FEATURES.get("tasks") and st.session_state.tools.get("Tasks"):
    st.header("📝 Your Task List")
    new_task = st.text_input("Add a new task")
    if st.button("➕ Add Task") and new_task.strip():
        tasks.add_task(new_task.strip())
        st.success(f"Added: {new_task}")
        st.rerun()

    for i, task in enumerate(tasks.load_tasks()):
        cols = st.columns([0.7, 0.2, 0.1])
        with cols[0]:
            checkbox = st.checkbox(task["text"], value=task["done"], key=f"task_{i}")
            if checkbox != task["done"]:
                tasks.toggle_task(i)
                st.rerun()
        with cols[2]:
            if st.button("🗑", key=f"delete_{i}"):
                tasks.delete_task(i)
                st.rerun()
