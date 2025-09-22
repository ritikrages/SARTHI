# ai/assistant.py (Cohere working version - clean and tested)

import cohere
from ai.voice import say

# ✅ Initialize Cohere client with your actual API key
co = cohere.Client("j8F4ajsTusxOnbJdLAuk3J7JBlFiTlwpLpcihd1x")

def multilingual_assistant(command=None, history=None, reset=False):
    say("Using Cohere model now.")

    if reset and history is not None:
        history.clear()
        say("Chat history reset.")
        return

    if not command:
        say("Please say something.")
        return

    history.append({"role": "user", "content": command})

    try:
        response = co.chat(
            message=command,
            model='command-r-plus',
            temperature=0.7
        )

        print("Cohere raw response:", response)

        answer = getattr(response, 'text', None)
        if not answer:
            say("No response from Cohere.")
            return

        history.append({"role": "assistant", "content": answer})

        clean_answer = answer.replace("\n", " ").strip()
        say(clean_answer)

    except Exception as e:
        say("Failed to connect to Cohere.")
        print("Cohere Error:", e)
