# ai/voice.py

import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty('rate', 170)

# Function to speak
def say(text):
    print(f"SARTHI: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to listen
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
        try:
            print("🔍 Recognizing...")
            command = r.recognize_google(audio, language="en-in")
            print(f"You said: {command}")
            return command.lower()
        except Exception as e:
            say("Sorry, I didn't catch that.")
            print("Recognition error:", e)
            return ""

# Function to switch voices based on language
def set_voice(language="en"):
    voices = engine.getProperty('voices')
    if language == "hi":  # Hindi
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        say("अब मैं हिंदी में बोलूंगा।")
    elif language == "bn":  # Bengali
        if len(voices) > 2:
            engine.setProperty('voice', voices[2].id)
        say("এখন আমি বাংলায় কথা বলব।")
    else:
        engine.setProperty('voice', voices[0].id)
        say("Switching back to English.")
