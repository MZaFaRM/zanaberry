import pygame

total_eye_calls = 0


def draw_tired(surface, x, y, width, height, color):
    global total_eye_calls

    # First call in a pair is Left (Even), second is Right (Odd)
    is_left_eye = total_eye_calls % 2 == 0

    # Since we draw 2 eyes per frame, dividing calls by 2 gives the true frame count
    current_frame = total_eye_calls // 2

    # Increment for the next call
    total_eye_calls += 1

    eye_height = max(12, int(height * 0.6))
    rect = pygame.Rect(int(x - width // 2), int(y), width, eye_height)
    pygame.draw.rect(surface, color, rect, border_radius=eye_height // 3)

    # Every 90 true frames, switch which side of the face sweats
    is_left_turn = (current_frame // 90) % 2 == 0

    # Only draw the sweat drop if it's THIS eye's turn to sweat
    if is_left_eye == is_left_turn:
        sweat_cycle = current_frame % 90
        slide_progress = sweat_cycle / 90.0

        # Start above the eye and slide down
        drop_y = int(y - height * 0.1 + slide_progress * (height * 1.5))

        # Drop falls on the outside edge of the face (left of the left eye, right of the right eye)
        drop_x = int(x - width * 0.7) if is_left_eye else int(x + width * 0.7)

        # Scale it up at the start, shrink it at the end
        if sweat_cycle < 15:
            scale = sweat_cycle / 15.0
        elif sweat_cycle > 75:
            scale = (90 - sweat_cycle) / 15.0
        else:
            scale = 1.0

        r = int(max(3, width // 10) * scale)

        if r > 0:
            pygame.draw.circle(surface, color, (drop_x, drop_y), r)
            top_point = (drop_x, drop_y - int(r * 2.5))
            left_point = (drop_x - r, drop_y)
            right_point = (drop_x + r, drop_y)
            pygame.draw.polygon(surface, color, [left_point, right_point, top_point])
