# ai/offline_assistant.py

from ai.voice import say

def offline_assistant(command: str):
    """
    Offline fallback assistant.
    Handles simple predefined commands without internet.
    """
    if not command:
        return

    command = command.lower()

    if "hello" in command:
        say("Hello! I am SARTHI, your offline assistant.")

    elif "how are you" in command:
        say("I am running perfectly in offline mode!")

    elif "play music" in command:
        say("Playing offline music is not supported yet.")

    elif "time" in command:
        import datetime
        now = datetime.datetime.now().strftime("%H:%M")
        say(f"The time is {now}")

    else:
        say("Sorry, I cannot understand that in offline mode.")
