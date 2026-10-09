def get_last_corner_min_speed(history: dict, steer_threshold: float = 0.15):
    speed = history["speed"]
    steer = history["steer"]

    corner_indices = {i for i, s in enumerate(steer) if abs(s) > steer_threshold}
    if not corner_indices:
        return None

    end = max(corner_indices)
    start = end
    while (start - 1) in corner_indices:
        start -= 1

    return min(speed[start:end + 1])
