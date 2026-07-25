import psutil

LAST_CHECK = 0
LAST_ZONE = "normal"
INTERVAL = 5000


def check_temp_zone(current_time, cold_threshold=45.0, hot_threshold=75.0, raise_exception=False):
    global LAST_CHECK, LAST_ZONE

    if current_time - LAST_CHECK > INTERVAL:
        LAST_CHECK = current_time
        try:
            temp = psutil.sensors_temperatures()["coretemp"][0].current

            if temp < cold_threshold:
                LAST_ZONE = "cold"
            elif temp > hot_threshold:
                LAST_ZONE = "hot"
            else:
                LAST_ZONE = "normal"

        except Exception:
            LAST_ZONE = "normal"
            if raise_exception:
                raise

    return LAST_ZONE
