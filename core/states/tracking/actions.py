import pygame

from core.states.tracking.faces import draw_tracking


def apply_tracking_effects(context):
    context.movement_multiplier = 1.8

    context.target_pos = pygame.mouse.get_pos()
    
    context.expressions["tracking"] = {
        "draw_fn": draw_tracking,
        "chance": 0.0,
        "duration_ms": 0,
    }

    if "tracking" in context.expressions:
        context.expression_override = "tracking"
