from core.states.base.state import State
from core.states.default.faces import Curious, Happy, Normal


class DefaultState(State):
    def __init__(self):
        super().__init__(priority=0)

        # Expressions
        self.normal = Normal()
        self.happy = Happy()
        self.curious = Curious()

    def is_active(self, current_time):
        return True

    def apply(self, context, current_time):
        context.expressions["normal"] = {
            "instance": self.normal,
            "chance": 0.0,
            "duration_ms": 0,
        }
        context.expressions["happy"] = {
            "instance": self.happy,
            "chance": 0.1,
            "duration_ms": 1500,
        }
        context.expressions["curious"] = {
            "instance": self.curious,
            "chance": 0.1,
            "duration_ms": 1500,
        }
