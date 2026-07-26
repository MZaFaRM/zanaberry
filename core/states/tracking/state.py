from core.states.base.state import State
from core.states.tracking.actions import apply_tracking_effects
from core.states.tracking.sensors import check_mouse_moving


class MouseTrackingState(State):
    def __init__(self):
        super().__init__(priority=5)

    def is_active(self, current_time):
        return check_mouse_moving(current_time)

    def apply(self, context, current_time):
        apply_tracking_effects(context)