from core.states.base.state import State
from core.states.temperature.actions import apply_cold_effects, apply_hot_effects
from core.states.temperature.sensors import check_temp_zone


class CPUTemperatureState(State):
    def __init__(self):
        super().__init__(priority=10)
        self.current_zone = "normal"

    def is_active(self, current_time):
        self.current_zone = check_temp_zone(current_time)
        
        return self.current_zone in ["cold", "hot"]

    def apply(self, context, current_time):
        if self.current_zone == "cold":
            apply_cold_effects(context)
        elif self.current_zone == "hot":
            apply_hot_effects(context)