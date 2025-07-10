# main.py
import streamlit as st
import streamlit.components.v1 as components
from utils.config import FEATURES, VOICE_ENABLED
from modules import chat, news, markets, voice, tasks, weather, memory, wake

# ✅ Browser-based TTS (mobile safe)
def speak_browser(text: str):
    components.html(f"""
        <button id="speak-btn" style="display:none;" onclick="speakText()">Speak</button>
        <script>
            function speakText() {{
                const message = new SpeechSynthesisUtterance({text!r});
                message.lang = "en-US";
                message.pitch = 1;
                message.rate = 1;
                speechSynthesis.speak(message);
            }}
            document.addEventListener("click", function triggerOnce() {{
                const btn = document.getElementById("speak-btn");
                if (btn) {{
                    btn.click();
                }}
                document.removeEventListener("click", triggerOnce);
            }});
        </script>
    """, height=0)

st.set_page_config(
    page_title="Mini-JARVIS",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("### 🎛 Voice Settings")

if "voice_enabled" not in st.session_state:
    st.session_state["voice_enabled"] = True
st.session_state["voice_enabled"] = st.sidebar.toggle("🔊 Enable Voice", value=True)
voice_gender = st.sidebar.selectbox("🗣 Select Voice", ["Default", "Male", "Female"])

st.write("✅ Task section loaded")
st.title("🤖 Mini-JARVIS — Your Local AI Assistant")

# Chat
if FEATURES["chat"]:
    st.header("🧠 Chat with GPT")
    user_prompt = st.text_input("You:", key="chat_input")
    if user_prompt:
        response = chat.ask_gpt(user_prompt)
        st.write("Jarvis:", response)
        if st.session_state["voice_enabled"]:
            st.markdown("📱 On mobile, tap anywhere to enable voice")
            speak_browser(response)

# Wake Word
if FEATURES.get("voice", True):
    st.header("🎙 Wake Word Listening")
    if st.button("🔊 Start Listening"):
        st.info("Listening for 'Hey Jarvis'...")
        if wake.listen_for_wake_word():
            st.success("✅ Wake word detected!")
            transcript = voice.transcribe_voice()
            st.write("You said:", transcript)
            response = chat.ask_gpt(transcript)
            st.write("Jarvis:", response)
            if st.session_state["voice_enabled"]:
                speak_browser(response)
        else:
            st.warning("Wake word not detected.")

# News
if FEATURES["news"]:
    st.header("📰 News Summary")
    news_data = news.get_top_headlines()
    for article in news_data:
        st.markdown(f"**{article['title']}**\n\n{article['description']}\n")

# Markets
if FEATURES["markets"]:
    st.header("📈 Market Tracker")
    st.line_chart(markets.get_stock_data("AAPL"))

# Tasks
st.header("📝 Your Task List")
new_task = st.text_input("Add a new task")
if st.button("➕ Add Task") and new_task.strip():
    tasks.add_task(new_task.strip())
    st.success(f"Added task: {new_task}")
    st.rerun()

task_list = tasks.load_tasks()
for i, task in enumerate(task_list):
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

# Weather
if FEATURES.get("weather", True):
    st.header("🌤️ Weather")
    city = st.text_input("Enter city name", value="Delhi", key="weather_city")
    if st.button("Get Weather"):
        report = weather.get_weather(city)
        st.success(report)
