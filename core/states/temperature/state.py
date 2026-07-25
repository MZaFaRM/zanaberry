from core.states.base.state import State
from core.states.temperature.actions import apply_tired_effects
from core.states.temperature.sensors import check_resource_zone


class ResourceIntensive(State):
    def __init__(self):
        super().__init__(priority=10)
        self.current_zone = "normal"

    def is_active(self, current_time):
        self.current_zone = check_resource_zone(current_time)

        return self.current_zone == "hot"

    def apply(self, context, current_time):
        if self.current_zone == "hot":
            apply_tired_effects(context)
