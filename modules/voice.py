import speech_recognition as sr

def transcribe_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=5)
        return recognizer.recognize_google(audio, language="en-IN")
    except sr.WaitTimeoutError:
        return "(Timeout: no speech detected)"
    except sr.UnknownValueError:
        return "(Could not understand audio)"
    except Exception as e:
        return f"(Error: {e})"
