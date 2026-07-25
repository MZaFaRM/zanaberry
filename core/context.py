from settings import CYAN


class StateContext:
    def __init__(self):
        self.color = CYAN
        self.movement_multiplier = 1.0
        self.expression_override = None 
        self.artifacts = []
        
        # Holds the expression configuration for the current frame
        # Format: {"name": {"instance": obj, "chance": float, "duration_ms": int}}
        self.expressions = {}