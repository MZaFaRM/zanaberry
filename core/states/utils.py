import math

import pygame


def check_blink():
    """Returns True for 150ms every 3.5 seconds to create a natural blink."""
    ticks = pygame.time.get_ticks()
    return (ticks % 3500) < 150


def get_darting_gaze():
    """Returns pseudo-random (nx, ny) coordinates that update every 1.2 seconds."""
    ticks = pygame.time.get_ticks()
    phase = ticks // 1200  # Change gaze every 1.2 seconds

    # Generate stateless pseudo-random numbers based on the time phase
    seed1 = (phase * 17) % 100
    seed2 = (phase * 31) % 100

    if seed1 < 60:
        # 60% of the time, just rest looking straight ahead
        return 0.0, 0.0

    # Otherwise, dart to a random angle
    angle = (seed2 / 100.0) * math.pi * 2
    intensity = 0.6  # Limit intensity so they don't roll into the back of the head
    return math.cos(angle) * intensity, math.sin(angle) * intensity
