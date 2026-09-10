# F1 Engineer Assistant

This is a small project I made to work with F1 25 telemetry data.

The program listens to the game's UDP telemetry, parses some of the car data and sends a summary to Gemini. The idea is to get simple race engineer style feedback while driving.

Right now I'm using data such as speed, throttle, brake, RPM, gear and tyre temperatures.

I also added a basic Matplotlib dashboard to see some of the telemetry live.

## Run

Install the dependencies:

```bash
pip install google-genai matplotlib
```

Set your Gemini API key:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Enable UDP telemetry in F1 25 and use port `20777`.

Then run:

```bash
python main.py
```

It's still a work in progress. I want to add more telemetry data and improve the feedback later.
