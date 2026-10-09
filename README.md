# F1 Race Engineer

A Python project that reads live UDP telemetry from F1 25, displays it on a
Matplotlib dashboard, and feeds it to an OpenAI-powered race engineer that
gives you short, spoken advice during a session.

## How it works

- **`telemetry/`** — listens for UDP packets on port `20777`, parses them,
  and keeps the latest values plus a short rolling history in a thread-safe
  shared state. Packets handled: Session, Lap Data, Car Telemetry, Car
  Status, Car Damage, and the Event packet (used to detect a button press).
- **`ui/`** — a Matplotlib dashboard showing speed, throttle/brake, RPM, tyre
  age, and brake/tyre temperatures in real time.
- **`ai/`** — a race engineer built on the OpenAI API. It only sends what
  changed since the last update plus any critical alerts (low fuel, heavy
  damage, safety car, etc.), so advice stays specific instead of generic. It
  also looks at recent steering/speed history to report how much speed you
  carried through the last corner. Advice is printed to the console and read
  aloud (macOS `say`).

The race engineer speaks automatically every 30 seconds, or immediately when
you press a button bound to **UDP Action 1** in-game.

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

2. Create a `.env` file (see `.env.example`) with your OpenAI API key and
   model:

   ```
   OPENAI_API_KEY=your-key-here
   OPENAI_MODEL=gpt-4o-mini
   ```

   `OPENAI_MODEL` is optional — if you leave it out, `gpt-4o-mini` is used
   by default.

3. In F1 25, go to **Settings → Telemetry Settings** and set:
   - UDP Telemetry: On
   - UDP IP Address: the IP of the machine running this script (`127.0.0.1`
     if it's the same machine)
   - UDP Port: `20777`
   - UDP Format: 2025

4. To trigger advice on demand (instead of waiting for the 30-second cycle),
   go to **Settings → Controls** in F1 25 and bind a free button to
   **UDP Action 1**. The app listens for that specific control, not for any
   particular physical button — pressing whatever you bind to it immediately
   asks the race engineer for advice.

## Run

```bash
.venv/bin/python main.py
```

I built this project mainly to understand how F1 telemetry packets work and
to practice working with binary data, UDP sockets, and LLM integrations in
Python.
