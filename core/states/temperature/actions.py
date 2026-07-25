def apply_cold_effects(context):
    context.color = (150, 220, 255)
    context.movement_multiplier = 0.2

    if "happy" in context.expressions:
        context.expressions["happy"]["chance"] = 0.6


def apply_hot_effects(context):
    context.color = (255, 100, 100)
    context.movement_multiplier = 2.5

    if "happy" in context.expressions:
        context.expressions["happy"]["chance"] = 0.05
    if "curious" in context.expressions:
        context.expressions["curious"]["chance"] = 0.5
