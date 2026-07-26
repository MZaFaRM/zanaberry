import pygame


def draw_happy(surface, x, y, face_width, face_height, color):
    # Happy eyes (^ ^)
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

    mouth_w = int(face_width * 0.2)
    mouth_h = int(face_height * 0.07)

    mouth_points = [
        (int(x - mouth_w), mouth_y),  # Top left
        (int(x - mouth_w // 2), mouth_y + mouth_h),  # Bottom left curve
        (int(x), mouth_y + mouth_h // 3),  # Middle peak
        (int(x + mouth_w // 2), mouth_y + mouth_h),  # Bottom right curve
        (int(x + mouth_w), mouth_y),  # Top right
    ]
    pygame.draw.lines(surface, color, False, mouth_points, width=line_w)
