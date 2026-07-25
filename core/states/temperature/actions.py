from core.states.temperature.faces import draw_tired


def apply_tired_effects(context):
    # Thermal Throttling: The system is struggling and lagging
    context.color = (255, 60, 60)  # Warning red
    context.movement_multiplier = 0.1  # Barely moving, severe lag
    context.expressions["tired"] = {
        "draw_fn": draw_tired,
        "chance": 0.0,
        "duration_ms": 0,
    }

    context.expression_override = "tired"

    # A throttling CPU is definitely not happy
    if "happy" in context.expressions:
        context.expressions["happy"]["chance"] = 0.0

    # It just stares blankly, trying to process
    if "curious" in context.expressions:
        context.expressions["curious"]["chance"] = 0.0
