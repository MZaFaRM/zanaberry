class State:
    """Blueprint for all system states. Modifies the context payload each frame."""

    def __init__(self, priority=10):
        """Sets execution order. Higher priority states run last and overwrite lower ones."""
        self.priority = priority

    def is_active(self, current_time):
        """Returns True if this state should influence the engine this frame."""
        return False

    def apply(self, context, current_time):
        """Modifies the shared context payload (colors, expressions, multipliers)."""
