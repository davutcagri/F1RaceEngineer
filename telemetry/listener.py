import struct
from socket import socket, AF_INET, SOCK_DGRAM

from . import packets, state

_last_button_status = 0


def listen(port: int = 20777) -> None:
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', port))

    while True:
        data, _ = server_socket.recvfrom(4096)
        if len(data) < packets.HEADER_SIZE:
            continue

        header = struct.unpack_from(packets.HEADER_FORMAT, data, 0)
        packet_id = header[5]
        player_idx = header[10]

        if packet_id == packets.CAR_TELEMETRY_PACKET_ID:
            _handle_car_telemetry(data, player_idx)
        elif packet_id == packets.CAR_STATUS_PACKET_ID:
            _handle_car_status(data, player_idx)
        elif packet_id == packets.LAP_DATA_PACKET_ID:
            _handle_lap_data(data, player_idx)
        elif packet_id == packets.CAR_DAMAGE_PACKET_ID:
            _handle_car_damage(data, player_idx)
        elif packet_id == packets.SESSION_PACKET_ID:
            _handle_session(data)
        elif packet_id == packets.EVENT_PACKET_ID:
            _handle_event(data)


def _handle_car_telemetry(data: bytes, player_idx: int) -> None:
    offset = packets.HEADER_SIZE + (player_idx * packets.TELEM_ENTRY_SIZE)
    speed, throttle, steer, brake, clutch, gear, rpm = struct.unpack_from(
        packets.TELEM_ENTRY_FORMAT, data, offset
    )
    brakes_temp = list(struct.unpack_from('<4H', data, offset + 22))
    tyres_temp = list(struct.unpack_from('<4B', data, offset + 30))

    state.record_snapshot({
        "speed": speed,
        "throttle": int(throttle * 100),
        "steer": round(steer, 2),
        "brake": int(brake * 100),
        "gear": gear,
        "rpm": rpm,
        "brakes_temperature": brakes_temp,
        "tyres_surface_temp": tyres_temp,
    })


def _handle_car_status(data: bytes, player_idx: int) -> None:
    offset = packets.HEADER_SIZE + (player_idx * packets.CAR_STATUS_ENTRY_SIZE)
    (
        traction_control,
        anti_lock_brakes,
        fuel_mix,
        front_brake_bias,
        pit_limiter_status,
        fuel_in_tank,
        fuel_capacity,
        fuel_remaining_laps,
        max_rpm,
        idle_rpm,
        max_gears,
        drs_allowed,
        drs_activation_distance,
        actual_tyre_compound,
        visual_tyre_compound,
        tyre_age,
        vehicle_fia_flags,
        engine_power_ice,
        engine_power_mguk,
        ers_store_energy,
        ers_deploy_mode,
        ers_harvested_this_lap_mguk,
        ers_harvested_this_lap_mguh,
        ers_deployed_this_lap,
        network_paused,
    ) = struct.unpack_from(packets.CAR_STATUS_ENTRY_FORMAT, data, offset)

    state.update_fields({
        "traction_control": traction_control,
        "anti_lock_brakes": anti_lock_brakes,
        "fuel_mix": fuel_mix,
        "front_brake_bias": front_brake_bias,
        "pit_limiter_status": pit_limiter_status,
        "fuel_in_tank": fuel_in_tank,
        "fuel_capacity": fuel_capacity,
        "fuel_remaining_laps": fuel_remaining_laps,
        "max_rpm": max_rpm,
        "idle_rpm": idle_rpm,
        "max_gears": max_gears,
        "drs_allowed": drs_allowed,
        "drs_activation_distance": drs_activation_distance,
        "actual_tyre_compound": actual_tyre_compound,
        "visual_tyre_compound": visual_tyre_compound,
        "tyre_age": tyre_age,
        "vehicle_fia_flags": vehicle_fia_flags,
        "engine_power_ice": engine_power_ice,
        "engine_power_mguk": engine_power_mguk,
        "ers_store_energy": ers_store_energy,
        "ers_deploy_mode": ers_deploy_mode,
        "ers_harvested_this_lap_mguk": ers_harvested_this_lap_mguk,
        "ers_harvested_this_lap_mguh": ers_harvested_this_lap_mguh,
        "ers_deployed_this_lap": ers_deployed_this_lap,
    })


def _handle_lap_data(data: bytes, player_idx: int) -> None:
    offset = packets.HEADER_SIZE + (player_idx * packets.LAP_DATA_ENTRY_SIZE)
    (
        last_lap_time_ms,
        current_lap_time_ms,
        sector1_time_ms_part,
        sector1_time_minutes_part,
        sector2_time_ms_part,
        sector2_time_minutes_part,
        delta_to_car_in_front_ms_part,
        delta_to_car_in_front_minutes_part,
        delta_to_race_leader_ms_part,
        delta_to_race_leader_minutes_part,
        lap_distance,
        total_distance,
        safety_car_delta,
        car_position,
        current_lap_num,
        pit_status,
        num_pit_stops,
        sector,
        current_lap_invalid,
        penalties,
        total_warnings,
        corner_cutting_warnings,
        num_unserved_drive_through_pens,
        num_unserved_stop_go_pens,
        grid_position,
        driver_status,
        result_status,
        pit_lane_timer_active,
        pit_lane_time_in_lane_ms,
        pit_stop_timer_ms,
        pit_stop_should_serve_pen,
        speed_trap_fastest_speed,
        speed_trap_fastest_lap,
    ) = struct.unpack_from(packets.LAP_DATA_ENTRY_FORMAT, data, offset)

    state.update_fields({
        "last_lap_time_ms": last_lap_time_ms,
        "current_lap_time_ms": current_lap_time_ms,
        "sector1_time_ms_part": sector1_time_ms_part,
        "sector1_time_minutes_part": sector1_time_minutes_part,
        "sector2_time_ms_part": sector2_time_ms_part,
        "sector2_time_minutes_part": sector2_time_minutes_part,
        "lap_distance": lap_distance,
        "total_distance": total_distance,
        "safety_car_delta": safety_car_delta,
        "car_position": car_position,
        "current_lap_num": current_lap_num,
        "pit_status": pit_status,
        "num_pit_stops": num_pit_stops,
        "sector": sector,
        "current_lap_invalid": current_lap_invalid,
        "penalties": penalties,
        "total_warnings": total_warnings,
        "corner_cutting_warnings": corner_cutting_warnings,
        "num_unserved_drive_through_pens": num_unserved_drive_through_pens,
        "num_unserved_stop_go_pens": num_unserved_stop_go_pens,
        "grid_position": grid_position,
        "driver_status": driver_status,
        "result_status": result_status,
        "pit_lane_time_in_lane_ms": pit_lane_time_in_lane_ms,
        "pit_stop_timer_ms": pit_stop_timer_ms,
        "speed_trap_fastest_speed": speed_trap_fastest_speed,
        "speed_trap_fastest_lap": speed_trap_fastest_lap,
    })


def _handle_car_damage(data: bytes, player_idx: int) -> None:
    offset = packets.HEADER_SIZE + (player_idx * packets.CAR_DAMAGE_ENTRY_SIZE)
    values = struct.unpack_from(packets.CAR_DAMAGE_ENTRY_FORMAT, data, offset)

    tyres_wear = list(values[0:4])
    tyres_damage = list(values[4:8])
    brakes_damage = list(values[8:12])
    tyre_blisters = list(values[12:16])
    (
        front_left_wing_damage,
        front_right_wing_damage,
        rear_wing_damage,
        floor_damage,
        diffuser_damage,
        sidepod_damage,
        drs_fault,
        ers_fault,
        gear_box_damage,
        engine_damage,
        engine_mguh_wear,
        engine_es_wear,
        engine_ce_wear,
        engine_ice_wear,
        engine_mguk_wear,
        engine_tc_wear,
        engine_blown,
        engine_seized,
    ) = values[16:34]

    state.update_fields({
        "tyres_wear": tyres_wear,
        "tyres_damage": tyres_damage,
        "brakes_damage": brakes_damage,
        "tyre_blisters": tyre_blisters,
        "front_left_wing_damage": front_left_wing_damage,
        "front_right_wing_damage": front_right_wing_damage,
        "rear_wing_damage": rear_wing_damage,
        "floor_damage": floor_damage,
        "diffuser_damage": diffuser_damage,
        "sidepod_damage": sidepod_damage,
        "drs_fault": drs_fault,
        "ers_fault": ers_fault,
        "gear_box_damage": gear_box_damage,
        "engine_damage": engine_damage,
        "engine_mguh_wear": engine_mguh_wear,
        "engine_es_wear": engine_es_wear,
        "engine_ce_wear": engine_ce_wear,
        "engine_ice_wear": engine_ice_wear,
        "engine_mguk_wear": engine_mguk_wear,
        "engine_tc_wear": engine_tc_wear,
        "engine_blown": engine_blown,
        "engine_seized": engine_seized,
    })


def _handle_session(data: bytes) -> None:
    (
        weather,
        track_temperature,
        air_temperature,
        total_laps,
        track_length,
        session_type,
        track_id,
        formula,
        session_time_left,
        session_duration,
        pit_speed_limit,
        game_paused,
        is_spectating,
        spectator_car_index,
        sli_pro_native_support,
        num_marshal_zones,
    ) = struct.unpack_from(packets.SESSION_LEADING_FORMAT, data, packets.HEADER_SIZE)

    safety_car_status, network_game = struct.unpack_from(
        packets.SESSION_SAFETY_CAR_FORMAT,
        data,
        packets.HEADER_SIZE + packets.SESSION_SAFETY_CAR_OFFSET,
    )

    state.update_fields({
        "weather": weather,
        "track_temperature": track_temperature,
        "air_temperature": air_temperature,
        "total_laps": total_laps,
        "track_length": track_length,
        "session_type": session_type,
        "track_id": track_id,
        "formula": formula,
        "session_time_left": session_time_left,
        "session_duration": session_duration,
        "pit_speed_limit": pit_speed_limit,
        "game_paused": game_paused,
        "safety_car_status": safety_car_status,
    })


def _handle_event(data: bytes) -> None:
    global _last_button_status

    event_code = struct.unpack_from(packets.EVENT_CODE_FORMAT, data, packets.HEADER_SIZE)[0]
    if event_code != packets.BUTTON_STATUS_EVENT_CODE:
        return

    (button_status,) = struct.unpack_from(
        packets.BUTTON_STATUS_FORMAT, data, packets.HEADER_SIZE + packets.EVENT_CODE_SIZE
    )
    pressed_now = bool(button_status & packets.TRIGGER_BUTTON_BIT)
    pressed_before = bool(_last_button_status & packets.TRIGGER_BUTTON_BIT)
    _last_button_status = button_status

    if pressed_now and not pressed_before:
        state.request_advice()
