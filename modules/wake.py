import speech_recognition as sr

def listen_for_wake_word(wake_words=["hey jarvis", "okay jarvis"], timeout=5):
    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        print("🎤 Mic initialized:", mic.device_index)

        with mic as source:
            print("🔧 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎧 Listening now...")
            audio = recognizer.listen(source, timeout=timeout)

        print("✅ Got audio input.")
        phrase = recognizer.recognize_google(audio, language="en-IN").lower().strip()
        print("📢 You said:", phrase)

        for wake in wake_words:
            if wake in phrase:
                print("✅ Wake word matched:", wake)
                return True

        return False

    except sr.WaitTimeoutError:
        print("⏱ Timeout: No voice detected")
        return False
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return False
    except Exception as e:
        print(f"🔥 Mic error:", e)
        return False

