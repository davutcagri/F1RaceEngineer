SYSTEM_PROMPT = (
    "You are a Formula 1 race engineer. You receive the driver's current "
    "status, what changed since the last update, and any active alerts. "
    "Give short, specific, actionable advice in English based on what is "
    "notable right now - avoid generic tips if nothing stands out. Keep it "
    "brief - no more than 2-3 sentences."
)


def build_user_prompt(context: dict) -> str:
    lines = ["Current status:"]
    for key, value in context["current"].items():
        lines.append(f"- {key}: {value}")

    if context["changes"]:
        lines.append("\nChanges since last update:")
        for key, change in context["changes"].items():
            lines.append(f"- {key}: {change['from']} -> {change['to']}")

    if context["alerts"]:
        lines.append("\nAlerts:")
        for alert in context["alerts"]:
            lines.append(f"- {alert}")

    lines.append(
        "\nBased on this, give the driver a short, specific piece of advice. "
        "Focus on what changed or what needs attention."
    )
    return "\n".join(lines)
