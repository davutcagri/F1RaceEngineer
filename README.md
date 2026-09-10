# F1 Telemetry System

A small Python project for reading live telemetry data from F1 25.

The application listens to UDP packets from the game, parses telemetry data from the player's car and displays it using Matplotlib.

Currently it shows data such as speed, throttle, brake, RPM, gear and tyre temperatures.

## Run

Enable UDP telemetry in F1 25 and use port `20777`.

Then run:

```bash
python main.py
```

I built this project mainly to understand how F1 telemetry packets work and to practice working with binary data and UDP sockets in Python.
