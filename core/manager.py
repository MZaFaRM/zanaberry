from core.context import StateContext


class StateManager:
    def __init__(self):
        self.states = []

    def register_state(self, state):
        """Adds a new state to the manager."""
        self.states.append(state)

    def resolve(self, current_time):
        """Creates a fresh context and passes it through all active states by priority."""
        context = StateContext()

        active_states = [s for s in self.states if s.is_active(current_time)]
        active_states.sort(key=lambda s: s.priority)

        for state in active_states:
            state.apply(context, current_time)

        return context
