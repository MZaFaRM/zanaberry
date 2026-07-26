import pygame


def draw_normal(surface, x, y, width, height, color):
    rect = pygame.Rect(int(x - width // 2), int(y - height // 2), width, int(height))
    pygame.draw.rect(surface, color, rect, border_radius=10)

    pupil_width = int(width * 0.4)
    pupil_height = int(height * 0.4)
    pupil_rect = pygame.Rect(
        int(x - pupil_width // 2), int(y - pupil_height // 2), pupil_width, pupil_height
    )
    pygame.draw.rect(surface, (35, 35, 45), pupil_rect, border_radius=5)

    highlight_r = max(2, pupil_width // 6)
    pygame.draw.circle(
        surface,
        (255, 255, 255),
        (int(x - pupil_width * 0.18), int(y - pupil_height * 0.22)),
        highlight_r,
    )


def draw_happy(surface, x, y, width, height, color):
    rect = pygame.Rect(int(x - width // 2), int(y - height // 2 + 40), width, width)
    pygame.draw.arc(surface, color, rect, 0, 3.14159, 15)


DRAWING_LEFT = True


def draw_curious(surface, x, y, width, height, color):
    global DRAWING_LEFT

    actual_height = int(height) if DRAWING_LEFT else int(height * 0.5)

    rect = pygame.Rect(
        int(x - width // 2), int(y - actual_height // 2), width, actual_height
    )
    pygame.draw.rect(surface, color, rect, border_radius=10)

    pupil_width = int(width * 0.4)
    pupil_height = int(actual_height * 0.4)

    pupil_rect = pygame.Rect(
        int(x - pupil_width // 2), int(y - pupil_height // 2), pupil_width, pupil_height
    )
    pygame.draw.rect(surface, (35, 35, 45), pupil_rect, border_radius=5)

    # Highlight
    highlight_r = max(2, pupil_width // 6)
    pygame.draw.circle(
        surface,
        (255, 255, 255),
        (int(x - pupil_width * 0.18), int(y - pupil_height * 0.22)),
        highlight_r,
    )

    # Flip the global variable for the next eye
    DRAWING_LEFT = not DRAWING_LEFT
