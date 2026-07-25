import psutil

LAST_CHECK = 0
LAST_ZONE = "normal"
INTERVAL = 5000


def check_resource_zone(
    current_time,
    temp_threshold=75.0,
    cpu_threshold=85.0,
    ram_threshold=85.0,
    raise_exception=False,
):
    global LAST_CHECK, LAST_ZONE

    if current_time - LAST_CHECK > INTERVAL:
        LAST_CHECK = current_time
        try:
            # Check CPU Usage (%)
            # interval=None ensures it doesn't block the game loop
            cpu_usage = psutil.cpu_percent(interval=None)

            # Check RAM Usage (%)
            ram_usage = psutil.virtual_memory().percent

            # Check Temperature (Graceful fallback if hardware doesn't support it)
            temps = psutil.sensors_temperatures()
            if temps.get("coretemp"):
                temp = temps["coretemp"][0].current
            elif temps:  # Fallback to the first available sensor
                temp = next(iter(temps.values()))[0].current
            # If ANY resource is pushing its limits, the system is exhausted
            if (
                temp > temp_threshold
                or cpu_usage > cpu_threshold
                or ram_usage > ram_threshold
            ):
                LAST_ZONE = "hot"
            else:
                LAST_ZONE = "normal"

        except Exception:
            LAST_ZONE = "normal"
            if raise_exception:
                raise

    return LAST_ZONE
