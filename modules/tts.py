
# modules/tts.py
import pyttsx3
import threading

def speak(text: str, gender: str = "Default"):
    def run_speech():
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        engine.setProperty('volume', 1.0)

        # Pick voice by gender
        voices = engine.getProperty('voices')
        selected_voice = None

        for voice in voices:
            if gender.lower() == "female" and "female" in voice.name.lower():
                selected_voice = voice.id
                break
            elif gender.lower() == "male" and "male" in voice.name.lower():
                selected_voice = voice.id
                break

        if selected_voice:
            engine.setProperty('voice', selected_voice)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    thread = threading.Thread(target=run_speech)
    thread.start()
