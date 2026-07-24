import pygame

from expressions.base import Expression


class Curious(Expression):
    def __init__(self):
        super().__init__()
        # State toggle to distinguish left (first call) and right (second call)
        self.drawing_left = True

    def draw_eye(self, surface, x, y, width, height, color):
        if self.drawing_left:
            # Base eye geometry for left eye (squinted, resting lower)
            eye_height = max(10, height // 2)
            rect = pygame.Rect(int(x - width // 2), int(y), width, int(eye_height))
            pygame.draw.rect(surface, color, rect, border_radius=40)

        else:
            # Base eye geometry for right eye (wide open, shifted up)
            rect = pygame.Rect(int(x - width // 2), int(y - 10), width, int(height))
            pygame.draw.rect(surface, color, rect, border_radius=40)

            # Eyebrow dimensions and spatial anchors
            brow_thick = max(4, width // 8)
            brow_width = int(width * 1.3)
            brow_y_start = int(y - height // 2 - 25)
            brow_y_end = int(y - height // 2 - 45)

            # Angled raised eyebrow line (tilted upwards)
            start_pos = (int(x - brow_width // 2), brow_y_start)
            end_pos = (int(x + brow_width // 2), brow_y_end)
            pygame.draw.line(surface, color, start_pos, end_pos, brow_thick)

        # Toggle state for the engine's next draw call
        self.drawing_left = not self.drawing_left
