from ai.vision.greeting import run_greeting
from time import sleep

if __name__ == "__main__":
    print("🙋 Greeting test started...")
    run_greeting()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("🛑 Test stopped by user.")
