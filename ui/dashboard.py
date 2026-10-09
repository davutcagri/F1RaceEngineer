import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec

from telemetry.state import get_history, MAXLEN

MAX_SPEED = 0
BRAKE_LABELS = ["BFL", "BFR", "BRL", "BRR"]
TYRE_LABELS = ["FL", "FR", "RL", "RR"]

x = list(range(MAXLEN))

fig = plt.figure(figsize=(12, 8))
fig.suptitle("F1 25 Telemetry")
gs = GridSpec(3, 2, figure=fig)

ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])
ax4 = fig.add_subplot(gs[2, 0])
ax5 = fig.add_subplot(gs[2, 1])
brake_bars = ax4.bar(BRAKE_LABELS, [0, 0, 0, 0], color=['#ff4444', '#ff4444', '#ff8800', '#ff8800'])
tyre_bars = ax5.bar(TYRE_LABELS, [0, 0, 0, 0], color=['#0000ff', '#0000ff', '#0000ff', '#0000ff'])

line_speed,    = ax1.plot([], [], color="cyan",   label="Speed (km/h)")
line_throttle, = ax2.plot([], [], color="lime",   label="Throttle %")
line_brake,    = ax2.plot([], [], color="red",    label="Brake %")
line_rpm,      = ax3.plot([], [], color="orange", label="RPM")

ax1.set_ylim(0, 380);   ax1.set_xlim(0, MAXLEN); ax1.legend(); ax1.grid(alpha=0.3)
ax2.set_ylim(0, 110);   ax2.set_xlim(0, MAXLEN); ax2.legend(); ax2.grid(alpha=0.3)
ax3.set_ylim(3000, 14000); ax3.set_xlim(0, MAXLEN); ax3.legend(); ax3.grid(alpha=0.3)
ax4.set_ylim(0, 1000); ax4.set_ylabel("Brakes Temp (°C)"); ax4.grid(alpha=0.3, axis='y'); ax4.tick_params(axis='x', labelsize=12)
ax5.set_ylim(30, 200); ax5.set_ylabel("Tyres Surface Temp (°C)"); ax5.grid(alpha=0.3, axis='y'); ax5.tick_params(axis='x', labelsize=12)

max_speed_text = ax1.text(0.98, 0.95, "Max: 0 km/h", transform=ax1.transAxes, fontsize=12, fontweight="bold", color="black", ha="right", va="top")
tyre_age_text  = ax1.text(0.02, 0.95, "Tyre Age: 0 laps", transform=ax1.transAxes, fontsize=12, fontweight="bold", color="black", ha="left", va="top")


def _update(_):
    global MAX_SPEED

    history = get_history()

    current_speed = history["speed"][-1]
    if current_speed > MAX_SPEED:
        MAX_SPEED = current_speed
    max_speed_text.set_text(f"Max: {MAX_SPEED} km/h")
    tyre_age_text.set_text(f"Tyre Age: {history['tyre_age'][-1]} laps")

    line_speed.set_data(x, history["speed"])
    line_throttle.set_data(x, history["throttle"])
    line_brake.set_data(x, history["brake"])
    line_rpm.set_data(x, history["rpm"])

    for bar, temp in zip(brake_bars, history["brakes_temperature"][-1]):
        bar.set_height(temp)

    for bar, temp in zip(tyre_bars, history["tyres_surface_temp"][-1]):
        bar.set_height(temp)


def start() -> None:
    ani = animation.FuncAnimation(fig, _update, interval=50, blit=False, cache_frame_data=False)
    plt.tight_layout()
    plt.show()
