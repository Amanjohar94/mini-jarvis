# main.py
import streamlit as st
from st_chat_input_multimodal import multimodal_chat_input
from utils.config import FEATURES
from modules import chat, news, markets, tasks, weather
import os
import streamlit.components.v1 as components

# ✅ Universal voice support: desktop auto-play, mobile needs tap
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

# ✅ Speak via redirect trick: works on all platforms
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

# App layout
st.set_page_config(page_title="Mini-JARVIS", layout="wide", initial_sidebar_state="expanded")
st.sidebar.markdown("### 🌛 Voice Settings")

if "voice_enabled" not in st.session_state:
    st.session_state["voice_enabled"] = True
st.session_state["voice_enabled"] = st.sidebar.toggle("🔊 Enable Voice", value=True)
voice_gender = st.sidebar.selectbox("🗣 Select Voice", ["Default", "Male", "Female"])

st.title("🤖 Mini-JARVIS — Your Local AI Assistant")

# 💭 Chat
if FEATURES["chat"]:
    st.header("🧠 Chat with GPT")

    if "last_prompt" not in st.session_state:
        st.session_state["last_prompt"] = ""

    result = multimodal_chat_input(enable_voice_input=True, voice_language="en-US")

    if result:
        if "text" in result and result["text"]:
            spoken_text = result["text"]
            st.markdown(f"**You said:** {spoken_text}")
            response = chat.ask_gpt(spoken_text)
            st.write("Jarvis:", response)
            if st.session_state["voice_enabled"]:
                st.markdown("📱 Tap anywhere to enable voice on mobile")
                speak_browser(response)
        elif "audioFile" in result:
            st.audio(result["audioFile"])

# 📰 News
if FEATURES["news"]:
    st.header("📰 News Summary")
    for article in news.get_top_headlines():
        st.markdown(f"**{article['title']}**\n\n{article['description']}\n")

# 📈 Stock Chart
if FEATURES["markets"]:
    st.header("📈 Market Tracker")
    st.line_chart(markets.get_stock_data("AAPL"))

# 📝 Tasks
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

# 🌤️ Weather
if FEATURES.get("weather", True):
    st.header("🌤️ Weather")
    city = st.text_input("Enter city name", value="Delhi", key="weather_city")
    if st.button("Get Weather"):
        st.success(weather.get_weather(city))
