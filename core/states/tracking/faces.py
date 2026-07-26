import math

import pygame


def draw_tracking(surface, x, y, width, height, color):
    mx, my = pygame.mouse.get_pos()

    dx = mx - x
    dy = my - y
    distance = math.hypot(dx, dy)

    if distance > 0:
        nx = dx / distance
        ny = dy / distance
    else:
        nx, ny = 0, 0

    look_intensity = min(1.0, distance / 500.0)
    squish_factor = 1.0 - (abs(nx) * look_intensity * 0.3)
    current_width = int(width * squish_factor)

    rect = pygame.Rect(
        int(x - current_width // 2), int(y - height // 2), current_width, int(height)
    )
    pygame.draw.rect(surface, color, rect, border_radius=10)

    pupil_width = int(current_width * 0.4)
    pupil_height = int(height * 0.4)

    max_shift_x = (current_width - pupil_width) / 2.2
    max_shift_y = (height - pupil_height) / 2.2

    pupil_x = x + (nx * max_shift_x * look_intensity)
    pupil_y = y + (ny * max_shift_y * look_intensity)

    pupil_rect = pygame.Rect(
        int(pupil_x - pupil_width // 2),
        int(pupil_y - pupil_height // 2),
        pupil_width,
        pupil_height,
    )
    pygame.draw.rect(surface, (35, 35, 45), pupil_rect, border_radius=5)

    highlight_r = max(2, pupil_width // 6)
    pygame.draw.circle(
        surface,
        (255, 255, 255),
        (int(pupil_x - pupil_width * 0.18), int(pupil_y - pupil_height * 0.22)),
        highlight_r,
    )
