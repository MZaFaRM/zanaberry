import pygame

total_eye_calls = 0


def draw_tired(surface, x, y, width, height, color):
    global total_eye_calls

    is_left_eye = total_eye_calls % 2 == 0
    current_frame = total_eye_calls // 2
    total_eye_calls += 1

    actual_height = max(12, int(height * 0.5))
    rect = pygame.Rect(
        int(x - width // 2), int(y - actual_height // 2), width, actual_height
    )
    pygame.draw.rect(surface, color, rect, border_radius=10)

    pupil_width = int(width * 0.4)
    pupil_height = int(actual_height * 0.4)
    pupil_rect = pygame.Rect(
        int(x - pupil_width // 2),
        int(y - pupil_height // 2),
        pupil_width,
        pupil_height,
    )
    pygame.draw.rect(surface, (35, 35, 45), pupil_rect, border_radius=5)

    highlight_r = max(2, pupil_width // 6)
    pygame.draw.circle(
        surface,
        (255, 255, 255),
        (int(x - pupil_width * 0.18), int(y - pupil_height * 0.22)),
        highlight_r,
    )

    is_left_turn = (current_frame // 90) % 2 == 0

    if is_left_eye == is_left_turn:
        sweat_cycle = current_frame % 90
        slide_progress = sweat_cycle / 90.0

        drop_y = int(y - height * 0.1 + slide_progress * (height * 1.5))
        drop_x = int(x - width * 0.7) if is_left_eye else int(x + width * 0.7)

        if sweat_cycle < 15:
            scale = sweat_cycle / 15.0
        elif sweat_cycle > 75:
            scale = (90 - sweat_cycle) / 15.0
        else:
            scale = 1.0

        r = int(max(3, width // 10) * scale)

        if r > 0:
            # Use a light blue for the sweat drop instead of the eye's base color
            sweat_color = color

            pygame.draw.circle(surface, sweat_color, (drop_x, drop_y), r)
            top_point = (drop_x, drop_y - int(r * 2.5))
            left_point = (drop_x - r, drop_y)
            right_point = (drop_x + r, drop_y)
            pygame.draw.polygon(
                surface, sweat_color, [left_point, right_point, top_point]
            )
