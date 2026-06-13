import struct
from socket import socket, AF_INET, SOCK_DGRAM

HEADER_FORMAT = '<HBBBBBQfIIBB'
HEADER_SIZE   = struct.calcsize(HEADER_FORMAT)

TELEM_ENTRY_SIZE   = 60
TELEM_ENTRY_FORMAT = '<HfffBbH'

STATUS_ENTRY_SIZE     = 55
TYRE_AGE_FIELD_OFFSET = 27

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 20777))

_latest = {
    "speed": 0,
    "throttle": 0,
    "steer": 0,
    "brake": 0,
    "gear": 0,
    "rpm": 0,
    "tyre_age": 0,
    "brakes_temperature": [0, 0, 0, 0],
    "tyres_surface_temp": [0, 0, 0, 0]
}

def get_telemetry_data():
    while True:
        data, _ = server_socket.recvfrom(4096)
        if len(data) < HEADER_SIZE:
            continue

        header     = struct.unpack_from(HEADER_FORMAT, data, 0)
        packet_id  = header[5]
        player_idx = header[10]

        if packet_id == 6:
            offset = HEADER_SIZE + (player_idx * TELEM_ENTRY_SIZE)

            speed, throttle, steer, brake, clutch, gear, rpm = struct.unpack_from(TELEM_ENTRY_FORMAT, data, offset)
            brakes_temp = list(struct.unpack_from('<4H', data, offset + 22))
            tyres_temp = list(struct.unpack_from('<4B', data, offset + 30))

            _latest.update({
                "speed":    speed,
                "throttle": int(throttle * 100),
                "steer":    round(steer, 2),
                "brake":    int(brake * 100),
                "gear":     gear,
                "rpm":      rpm,
                "brakes_temperature": brakes_temp,
                "tyres_surface_temp": tyres_temp,
            })
            return dict(_latest)

        if packet_id == 7:
            offset = HEADER_SIZE + (player_idx * STATUS_ENTRY_SIZE) + TYRE_AGE_FIELD_OFFSET
            tyre_age = struct.unpack_from('<B', data, offset)[0]
            _latest["tyre_age"] = tyre_age