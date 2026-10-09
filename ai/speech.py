import subprocess

VOICE = "Daniel"


def speak(text: str) -> None:
    subprocess.run(["say", "-v", VOICE, text])
