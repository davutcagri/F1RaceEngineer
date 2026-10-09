import threading
from collections import deque

MAXLEN = 200

_lock = threading.Lock()
_has_data = False
_advice_requested = threading.Event()

_latest = {
    "speed": 0,
    "throttle": 0,
    "steer": 0,
    "brake": 0,
    "gear": 0,
    "rpm": 0,
    "tyre_age": 0,
    "brakes_temperature": [0, 0, 0, 0],
    "tyres_surface_temp": [0, 0, 0, 0],
}

_history = {
    "speed": deque([0] * MAXLEN, maxlen=MAXLEN),
    "steer": deque([0] * MAXLEN, maxlen=MAXLEN),
    "throttle": deque([0] * MAXLEN, maxlen=MAXLEN),
    "brake": deque([0] * MAXLEN, maxlen=MAXLEN),
    "rpm": deque([0] * MAXLEN, maxlen=MAXLEN),
    "tyre_age": deque([0] * MAXLEN, maxlen=MAXLEN),
    "brakes_temperature": deque([[0, 0, 0, 0]] * MAXLEN, maxlen=MAXLEN),
    "tyres_surface_temp": deque([[0, 0, 0, 0]] * MAXLEN, maxlen=MAXLEN),
}


def update_fields(fields: dict) -> None:
    global _has_data
    with _lock:
        _latest.update(fields)
        _has_data = True


def record_snapshot(fields: dict) -> dict:
    global _has_data
    with _lock:
        _latest.update(fields)
        _has_data = True
        snapshot = dict(_latest)
        for key in _history:
            _history[key].append(snapshot[key])
        return snapshot


def has_data() -> bool:
    with _lock:
        return _has_data


def request_advice() -> None:
    _advice_requested.set()


def wait_for_advice_trigger(timeout: float) -> None:
    _advice_requested.wait(timeout)
    _advice_requested.clear()


def get_latest() -> dict:
    with _lock:
        return dict(_latest)


def get_history() -> dict:
    with _lock:
        return {key: list(values) for key, values in _history.items()}
