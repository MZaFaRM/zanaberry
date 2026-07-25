from core.states.default.faces import draw_curious, draw_happy, draw_normal


def apply_default_effects(context):
    """Injects the baseline expressions and chances into the context."""
    context.expressions["normal"] = {
        "draw_fn": draw_normal,
        "chance": 0.0,
        "duration_ms": 0,
    }
    context.expressions["happy"] = {
        "draw_fn": draw_happy,
        "chance": 0.25,
        "duration_ms": 1500,
    }
    context.expressions["curious"] = {
        "draw_fn": draw_curious,
        "chance": 0.1,
        "duration_ms": 1500,
    }
