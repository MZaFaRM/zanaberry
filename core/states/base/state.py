class State:
    """
    Acts as a traffic director.

    A State's only job is to use external sensor functions to decide if it
    should be active, and if so, route the context to external action functions.
    """

    def __init__(self, priority=10):
        # Higher priority states run last and overwrite lower ones
        self.priority = priority

    def is_active(self, current_time):
        """Calls imported sensor functions to determine if this state should take over."""
        return False

    def apply(self, context, current_time):
        """Calls imported action functions to brutally overwrite the context."""
