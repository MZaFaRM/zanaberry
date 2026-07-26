import math

import pygame

from core.states.utils import check_blink


def draw_tracking(surface, x, y, face_width, face_height, color):
    eye_offset = int(face_width * 0.45)
    r = face_height // 4
    eye_y = int(y - face_height * 0.15)
    mouth_y = int(y + face_height * 0.25)
    line_w = 6

    if check_blink():
        for ex in [x - eye_offset, x + eye_offset]:
            pygame.draw.line(
                surface, color, (ex - r, eye_y), (ex + r, eye_y), width=line_w
            )
    else:
        mx, my = pygame.mouse.get_pos()
        for ex in [x - eye_offset, x + eye_offset]:
            pygame.draw.circle(surface, color, (ex, eye_y), r, width=line_w)

            dx, dy = mx - ex, my - eye_y
            distance = math.hypot(dx, dy)

            if distance > 0:
                nx, ny = dx / distance, dy / distance
            else:
                nx, ny = 0, 0

            pupil_r = max(3, r // 3)
            max_shift = r - pupil_r - (line_w // 2 + 1)
            look_intensity = min(1.0, distance / 200.0)

            cx = int(ex + nx * max_shift * look_intensity)
            cy = int(eye_y + ny * max_shift * look_intensity)

            pygame.draw.circle(surface, color, (cx, cy), pupil_r)

    # Mouth
    mouth_w = max(4, face_width // 10)
    pygame.draw.line(
        surface,
        color,
        (int(x - mouth_w), mouth_y),
        (int(x + mouth_w), mouth_y),
        width=line_w,
    )
