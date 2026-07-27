import math
import random

import pygame

from core.states.utils import check_blink, get_darting_gaze


def draw_normal(surface, x, y, face_width, face_height, color):
    eye_offset = int(face_width * 0.45)
    r = face_height // 4
    eye_y = int(y - face_height * 0.15)
    mouth_y = int(y + face_height * 0.25)
    line_w = 6

    nx, ny = get_darting_gaze()

    pupil_r = max(3, r // 3)
    max_shift = r - pupil_r - (line_w // 2 + 1)

    if check_blink():
        # Draw closed eyes
        for ex in [x - eye_offset, x + eye_offset]:
            pygame.draw.line(
                surface, color, (ex - r, eye_y), (ex + r, eye_y), width=line_w
            )
    else:
        # Draw open eyes
        for ex in [x - eye_offset, x + eye_offset]:
            pygame.draw.circle(surface, color, (ex, eye_y), r, width=line_w)
            cx = int(ex + nx * max_shift)
            cy = int(eye_y + ny * max_shift)
            pygame.draw.circle(surface, color, (cx, cy), pupil_r)

    gaze_distance = math.hypot(nx, ny)
    squish_factor = min(1.0, gaze_distance / 0.6)

    base_mouth_w = face_width // 4
    min_mouth_w = max(4, face_width // 10)

    mouth_w = int(base_mouth_w - (base_mouth_w - min_mouth_w) * squish_factor)

    pygame.draw.line(
        surface,
        color,
        (int(x - mouth_w), mouth_y),
        (int(x + mouth_w), mouth_y),
        width=line_w,
    )


def draw_happy(surface, x, y, face_width, face_height, color):
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

    nx, ny = 0.4, -0.5

    if check_blink():
        # LEFT EYE (Big)
        ex_left = x - eye_offset
        pygame.draw.line(
            surface, color, (ex_left - r, eye_y), (ex_left + r, eye_y), width=line_w
        )

        # RIGHT EYE (Small)
        ex_right = x + eye_offset
        r_right = r // 2
        eye_y_right = int(eye_y + r // 2)
        pygame.draw.line(
            surface,
            color,
            (ex_right - r_right, eye_y_right),
            (ex_right + r_right, eye_y_right),
            width=line_w,
        )
    else:
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


GLITCH_LAST_UPDATE = 0
GLITCH_DELAY = 20
GLITCH_STATE = None


def draw_glitch(surface, x, y, face_width, face_height, color):
    global GLITCH_LAST_UPDATE, GLITCH_DELAY, GLITCH_STATE

    current_time = pygame.time.get_ticks()

    if GLITCH_STATE is None or (current_time - GLITCH_LAST_UPDATE > GLITCH_DELAY):
        jitter = lambda: random.randint(-6, 6)
        shapes = ["circle", "rect", "line", "x"]

        GLITCH_STATE = {
            "left_shape": random.choice(shapes),
            "right_shape": random.choice(shapes),
            "left_eye_jitter": (jitter(), jitter()),
            "right_eye_jitter": (jitter(), jitter()),
            "left_pupil_jitter": (jitter(), jitter()),
            "right_pupil_jitter": (jitter(), jitter()),
        }

        GLITCH_LAST_UPDATE = current_time
        GLITCH_DELAY = random.randint(20, 150)

    eye_offset = int(face_width * 0.45)
    r = face_height // 4
    eye_y = int(y - face_height * 0.15)
    mouth_y = int(y + face_height * 0.25)
    line_w = max(2, face_width // 12)

    # Helper function to draw the chosen eye shape
    def draw_eye_shape(ex, shape, jx, jy):
        cx, cy = ex + jx, eye_y + jy
        if shape == "circle":
            pygame.draw.circle(surface, color, (cx, cy), r, width=line_w)
        elif shape == "rect":
            rect = pygame.Rect(0, 0, r * 2, r * 2)
            rect.center = (cx, cy)
            pygame.draw.rect(surface, color, rect, width=line_w)
        elif shape == "line":
            # A harsh horizontal slash
            pygame.draw.line(surface, color, (cx - r, cy), (cx + r, cy), width=line_w)
        elif shape == "x":
            # A jagged X
            pygame.draw.line(
                surface, color, (cx - r, cy - r), (cx + r, cy + r), width=line_w
            )
            pygame.draw.line(
                surface, color, (cx + r, cy - r), (cx - r, cy + r), width=line_w
            )

    ex_left = x - eye_offset
    left_shape = GLITCH_STATE["left_shape"]
    draw_eye_shape(ex_left, left_shape, *GLITCH_STATE["left_eye_jitter"])

    # Only draw pupil if it's not a line or X
    if left_shape not in ["line", "x"]:
        px, py = GLITCH_STATE["left_pupil_jitter"]
        pygame.draw.circle(surface, color, (ex_left + px, eye_y + py), max(2, r // 3))

    ex_right = x + eye_offset
    right_shape = GLITCH_STATE["right_shape"]
    draw_eye_shape(ex_right, right_shape, *GLITCH_STATE["right_eye_jitter"])

    # Only draw pupil if it's not a line or X
    if right_shape not in ["line", "x"]:
        px, py = GLITCH_STATE["right_pupil_jitter"]
        pygame.draw.circle(surface, color, (ex_right + px, eye_y + py), max(2, r // 3))

    mouth_w = face_width // 6
    pygame.draw.line(
        surface,
        color,
        (int(x - mouth_w), mouth_y),
        (int(x + mouth_w), mouth_y),
        width=line_w,
    )
