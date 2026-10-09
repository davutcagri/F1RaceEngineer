KEY_FIELDS = [
    "speed",
    "rpm",
    "fuel_in_tank",
    "fuel_remaining_laps",
    "tyre_age",
    "actual_tyre_compound",
    "tyres_wear",
    "last_corner_min_speed",
    "current_lap_num",
    "car_position",
    "pit_status",
    "num_pit_stops",
    "last_lap_time_ms",
    "penalties",
    "safety_car_status",
    "engine_damage",
    "gear_box_damage",
    "front_left_wing_damage",
    "front_right_wing_damage",
    "rear_wing_damage",
]

DELTA_THRESHOLDS = {
    "fuel_in_tank": 0.5,
    "fuel_remaining_laps": 0.3,
    "last_corner_min_speed": 5,
    "tyre_age": 1,
    "current_lap_num": 1,
    "car_position": 1,
    "num_pit_stops": 1,
    "last_lap_time_ms": 1,
    "penalties": 1,
}

ALERT_RULES = [
    ("fuel_remaining_laps", lambda v: v < 2, "Fuel is critically low - plan a pit stop."),
    ("engine_damage", lambda v: v >= 50, "Engine damage is high."),
    ("gear_box_damage", lambda v: v >= 50, "Gearbox damage is high."),
    ("front_left_wing_damage", lambda v: v >= 50, "Front left wing damage is high."),
    ("front_right_wing_damage", lambda v: v >= 50, "Front right wing damage is high."),
    ("rear_wing_damage", lambda v: v >= 50, "Rear wing damage is high."),
    ("safety_car_status", lambda v: v != 0, "Safety car is active."),
]

_previous = {}


def build_context(telemetry: dict) -> dict:
    global _previous

    current = {key: telemetry[key] for key in KEY_FIELDS if key in telemetry}

    changes = {}
    for key, value in current.items():
        previous_value = _previous.get(key)
        if previous_value is None or not _is_numeric(value):
            continue
        threshold = DELTA_THRESHOLDS.get(key, 0)
        if abs(value - previous_value) > threshold:
            changes[key] = {"from": previous_value, "to": value}

    alerts = [
        message
        for key, condition, message in ALERT_RULES
        if key in telemetry and condition(telemetry[key])
    ]

    _previous = current
    return {"current": current, "changes": changes, "alerts": alerts}


def _is_numeric(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)
