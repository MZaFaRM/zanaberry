from core.states.base.state import State
from core.states.default.actions import apply_default_effects
from core.states.default.sensors import check_always_active


class DefaultState(State):
    """The baseline state. Always runs first, sets up the default faces."""

    def __init__(self):
        super().__init__(priority=0)

    def is_active(self, current_time):
        return check_always_active(current_time)

    def apply(self, context, current_time):
        apply_default_effects(context)
