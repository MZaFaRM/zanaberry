from core.states.petting.faces import draw_happy


def apply_petting_effects(context):
    context.expressions["happy"] = {
        "draw_fn": draw_happy,
        "chance": 0.0,
        "duration_ms": 0,
    }

    if "happy" in context.expressions:
        context.expression_override = "happy"
