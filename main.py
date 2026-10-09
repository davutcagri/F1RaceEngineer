import threading

from dotenv import load_dotenv

from ai.assistant import get_advice
from ai.speech import speak
from telemetry import state
from telemetry.listener import listen
from ui.dashboard import start

load_dotenv()

ADVICE_INTERVAL_SECONDS = 30


def run_race_engineer() -> None:
    while True:
        state.wait_for_advice_trigger(ADVICE_INTERVAL_SECONDS)
        if not state.has_data():
            continue

        try:
            advice = get_advice()
            print(f"\n[Race Engineer] {advice}\n")
            speak(advice)
        except Exception as exc:
            print(f"\n[Race Engineer] Could not get advice: {exc}\n")


threading.Thread(target=listen, daemon=True).start()
threading.Thread(target=run_race_engineer, daemon=True).start()

start()
