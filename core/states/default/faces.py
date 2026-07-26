import math

import pygame

from core.states.utils import check_blink, get_darting_gaze


def draw_normal(surface, x, y, face_width, face_height, color):
    eye_offset = int(face_width * 0.45)
    r = face_height // 4
    eye_y = int(y - face_height * 0.15)
    mouth_y = int(y + face_height * 0.25)
    line_w = 6

    # Get the gaze direction first so both eyes and mouth can use it
    nx, ny = get_darting_gaze()

    if check_blink():
        # Draw closed eyes
        for ex in [x - eye_offset, x + eye_offset]:
            pygame.draw.line(
                surface, color, (ex - r, eye_y), (ex + r, eye_y), width=line_w
            )
    else:
        pupil_r = max(3, r // 3)
        max_shift = r - pupil_r - (line_w // 2 + 1)

        for ex in [x - eye_offset, x + eye_offset]:
            pygame.draw.circle(surface, color, (ex, eye_y), r, width=line_w)
            cx = int(ex + nx * max_shift)
            cy = int(eye_y + ny * max_shift)
            pygame.draw.circle(surface, color, (cx, cy), pupil_r)

    # Calculate how far the eyes are looking from center (0.0 to ~0.6)
    gaze_distance = math.hypot(nx, ny)

    # Normalize it to a 0.0 to 1.0 scale
    squish_factor = min(1.0, gaze_distance / 0.6)

    # Base width is relaxed, min width is pursed (like the tracking mouth)
    base_mouth_w = face_width // 4
    min_mouth_w = max(4, face_width // 10)

    # Shrink the mouth depending on the squish factor
    mouth_w = int(base_mouth_w - (base_mouth_w - min_mouth_w) * squish_factor)

    pygame.draw.line(
        surface,
        color,
        (int(x - mouth_w), mouth_y),
        (int(x + mouth_w), mouth_y),
        width=line_w,
    )


def draw_happy(surface, x, y, face_width, face_height, color):
    # Happy eyes are already closed (^ ^), so no blinking logic needed here!
    eye_offset = int(face_width * 0.45)
    r = face_height // 4
    eye_y = int(y - face_height * 0.15)
    mouth_y = int(y + face_height * 0.25)
    line_w = 8

    # Eyes: ^   ^
    for ex in [x - eye_offset, x + eye_offset]:
        points = [
            (int(ex - r), int(eye_y + r // 2)),
            (int(ex), int(eye_y - r // 2)),
            (int(ex + r), int(eye_y + r // 2)),
        ]
        pygame.draw.lines(surface, color, False, points, width=line_w)

    # Mouth
    mouth_w = face_width // 6
    pygame.draw.line(
        surface,
        color,
        (int(x - mouth_w), mouth_y),
        (int(x + mouth_w), mouth_y),
        width=line_w,
    )


def draw_curious(surface, x, y, face_width, face_height, color):
    eye_offset = int(face_width * 0.45)
    r = face_height // 4
    eye_y = int(y - face_height * 0.15)
    mouth_y = int(y + face_height * 0.25)
    line_w = 6

    if check_blink():
        # Blink for curious face (left is wider than right)
        pygame.draw.line(
            surface,
            color,
            (x - eye_offset - r, eye_y),
            (x - eye_offset + r, eye_y),
            width=line_w,
        )
        pygame.draw.line(
            surface,
            color,
            (x + eye_offset - r // 2, eye_y + r // 2),
            (x + eye_offset + r // 2, eye_y + r // 2),
            width=line_w,
        )
    else:
        # Fixed, subtle gaze direction: Up and slightly right
        nx, ny = 0.4, -0.5

        # LEFT EYE (Big)
        ex_left = x - eye_offset
        pygame.draw.circle(surface, color, (ex_left, eye_y), r, width=line_w)
        pupil_r_left = max(3, r // 3)
        shift_left = r - pupil_r_left - (line_w // 2 + 1)
        pygame.draw.circle(
            surface,
            color,
            (int(ex_left + nx * shift_left), int(eye_y + ny * shift_left)),
            pupil_r_left,
        )

        # RIGHT EYE (Small)
        ex_right = x + eye_offset
        r_right = r // 2
        eye_y_right = int(eye_y + r // 2)
        pygame.draw.circle(
            surface, color, (ex_right, eye_y_right), r_right, width=line_w
        )
        pupil_r_right = max(2, r_right // 3)
        shift_right = r_right - pupil_r_right - (line_w // 2 + 1)
        pygame.draw.circle(
            surface,
            color,
            (int(ex_right + nx * shift_right), int(eye_y_right + ny * shift_right)),
            pupil_r_right,
        )

    # Mouth: Tilted line /
    mouth_w = face_width // 5
    pygame.draw.line(
        surface,
        color,
        (int(x - mouth_w), mouth_y + 6),
        (int(x + mouth_w), mouth_y - 6),
        width=line_w,
    )
