from core.states.tracking.faces import draw_tracking


def apply_tracking_effects(context):
    context.expressions["tracking"] = {
        "draw_fn": draw_tracking,
        "chance": 0.0,
        "duration_ms": 0,
    }

    if "tracking" in context.expressions:
        context.expression_override = "tracking"
