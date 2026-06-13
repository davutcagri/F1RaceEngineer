import plot
import parser
import threading

def update_udp():
    while True:
        telemetry_data = parser.get_telemetry_data()
        if telemetry_data:
            plot.data_buffer["speed"].append(telemetry_data["speed"])
            plot.data_buffer["throttle"].append(telemetry_data["throttle"])
            plot.data_buffer["brake"].append(telemetry_data["brake"])
            plot.data_buffer["rpm"].append(telemetry_data["rpm"])
            plot.data_buffer["brakes_temperature"].append(telemetry_data["brakes_temperature"])
            plot.data_buffer["tyres_surface_temp"].append(telemetry_data["tyres_surface_temp"])
            plot.data_buffer["tyre_age"].append(telemetry_data["tyre_age"])

thread = threading.Thread(target=update_udp, daemon=True)
thread.start()

plot.start()