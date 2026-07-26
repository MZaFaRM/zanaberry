from core.states.base.state import State
from core.states.petting.actions import apply_petting_effects
from core.states.petting.sensors import check_petting


class PettingState(State):
    def __init__(self):
        super().__init__(priority=10)

    def is_active(self, current_time):
        return check_petting(current_time)

    def apply(self, context, current_time):
        apply_petting_effects(context)
