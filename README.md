<div align="center">

# F1 Telemetry System

A real-time telemetry dashboard that receives F1 25 UDP data and visualizes the player car's performance with Python and Matplotlib.

**Python · UDP Sockets · Binary Packet Parsing · Matplotlib**

> This project is an early-stage telemetry prototype built around the F1 25 UDP packet layout.

</div>

## About the project

F1 Telemetry System listens for telemetry packets sent by F1 25 over UDP port `20777`. It decodes binary car telemetry and car status packets, stores recent samples in rolling buffers, and displays the data on a live Matplotlib dashboard.

Telemetry collection runs on a background thread while the main thread renders and refreshes the dashboard.

## Features

- Receives live F1 25 telemetry over UDP
- Decodes the player car from binary telemetry packets
- Processes car telemetry packet ID `6`
- Processes car status packet ID `7`
- Displays a rolling speed graph
- Tracks maximum speed
- Displays throttle and brake input
- Displays engine RPM
- Displays individual brake temperatures
- Displays individual tyre surface temperatures
- Displays current tyre age in laps
- Keeps the latest 200 telemetry samples
- Refreshes the dashboard every 50 milliseconds

## Dashboard metrics

The dashboard currently visualizes:

| Metric | Visualization |
|---|---|
| Speed | Rolling line chart and maximum-speed value |
| Throttle | Rolling percentage chart |
| Brake | Rolling percentage chart |
| Engine RPM | Rolling line chart |
| Brake temperatures | FL, FR, RL, and RR bar chart |
| Tyre surface temperatures | FL, FR, RL, and RR bar chart |
| Tyre age | Current age in laps |

Wheel labels use the following abbreviations:

- `FL`: Front left
- `FR`: Front right
- `RL`: Rear left
- `RR`: Rear right

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Application and telemetry processing |
| UDP sockets | Receiving game telemetry |
| `struct` | Decoding binary packet data |
| Matplotlib | Real-time charts and dashboard |
| `deque` | Fixed-size rolling telemetry buffers |
| Threading | Running UDP collection in the background |

## Project structure

```text
F1TelemetrySystem/
├── main.py      # Starts the UDP worker and dashboard
├── parser.py    # Receives and decodes telemetry packets
└── plot.py      # Stores telemetry samples and renders the dashboard
```

## Requirements

- Python 3.10 or newer
- F1 25 with UDP telemetry enabled
- A graphical desktop environment for Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/davutcagri/F1TelemetrySystem.git
cd F1TelemetrySystem
```

Create and activate a virtual environment.

### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install Matplotlib:

```bash
python -m pip install matplotlib
```

## F1 25 telemetry configuration

Open the telemetry settings in F1 25 and configure them to match the application:

```text
UDP Telemetry: On
UDP IP Address: 127.0.0.1
UDP Port: 20777
UDP Format: 2025
```

The application binds to `0.0.0.0:20777`.

If the game is running on another device, replace `127.0.0.1` with the local network IP address of the computer running this application. You may also need to allow incoming UDP traffic on port `20777` through the firewall.

## Running the application

After activating the virtual environment, run:

```bash
python main.py
```

The application will start the UDP listener in a background thread and open the live telemetry dashboard.

Start or resume an on-track session in F1 25 to begin receiving data.

## How it works

1. F1 25 sends binary telemetry packets to UDP port `20777`.
2. `parser.py` reads the packet header and identifies the packet type.
3. Car telemetry packets update speed, throttle, brake, steering, gear, RPM, brake temperature, and tyre surface temperature.
4. Car status packets update tyre age.
5. `main.py` adds the latest values to fixed-size rolling buffers.
6. `plot.py` refreshes the charts and temperature bars every 50 milliseconds.

## Troubleshooting

### The dashboard opens but stays at zero

- Confirm that UDP telemetry is enabled in F1 25.
- Confirm that the UDP port is set to `20777`.
- Confirm that the UDP format is set to `2025`.
- Start or resume an on-track session.
- Check firewall permissions if the game runs on another device.
- Make sure no other application is already using UDP port `20777`.

### The application cannot bind to the port

Another telemetry application may already be listening on port `20777`. Close the other application or change the port in both F1 25 and `parser.py`.

### Matplotlib cannot open a window

The application requires a graphical desktop environment. It cannot display the dashboard in a headless terminal without an appropriate Matplotlib backend.

## Current limitations

- The parser is coupled to the F1 25 packet sizes and field offsets.
- Only car telemetry and car status packets are processed.
- Only the player car is visualized.
- Telemetry data is not persisted.
- Dashboard axis limits are currently fixed.
- Dependency versions are not yet pinned.

---

<div align="center">

Built as an experiment in real-time motorsport telemetry processing and visualization.

</div>
