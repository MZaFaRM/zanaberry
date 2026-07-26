import pygame


def draw_tired(surface, x, y, face_width, face_height, color):
    eye_offset = int(face_width * 0.45)
    r = face_height // 4
    eye_y = int(y - face_height * 0.15)
    mouth_y = int(y + face_height * 0.25)
    line_w = 6

    # Eyes: -   -
    for ex in [x - eye_offset, x + eye_offset]:
        pygame.draw.line(
            surface, color, (int(ex - r), eye_y), (int(ex + r), eye_y), width=line_w
        )

    # Mouth
    mouth_w = face_width // 3
    pygame.draw.line(
        surface,
        color,
        (int(x - mouth_w), mouth_y),
        (int(x + mouth_w), mouth_y),
        width=line_w,
    )

    # Sweat drop logic
    ticks = pygame.time.get_ticks()
    sweat_cycle = (ticks // 16) % 90
    slide_progress = sweat_cycle / 90.0

    if 10 < sweat_cycle < 80:
        drop_x = int(x - face_width * 0.65)
        drop_y = int(eye_y + slide_progress * (face_height * 0.8))
        drop_length = max(4, face_height // 6)
        pygame.draw.line(
            surface,
            color,
            (drop_x, drop_y),
            (drop_x, drop_y + drop_length),
            width=line_w - 2,
        )

