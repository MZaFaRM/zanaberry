import pygame

from expressions.base import Expression


class Curious(Expression):
    def __init__(self):
        super().__init__()
        # State toggle to distinguish left (first call) and right (second call)
        self.drawing_left = True

    def draw_eye(self, surface, x, y, width, height, color):
        if self.drawing_left:
            # Base eye geometry for left eye (scrutinizing narrow slit)
            eye_height = max(10, height // 3)
            rect = pygame.Rect(
                int(x - width // 2), int(y - eye_height // 2), width, int(eye_height)
            )
            pygame.draw.rect(surface, color, rect, border_radius=40)

        else:
            # Base eye geometry for right eye (wide open, shifted slightly up)
            rect = pygame.Rect(
                int(x - width // 2), int(y - height // 2 - 10), width, int(height)
            )
            pygame.draw.rect(surface, color, rect, border_radius=40)

            # Smooth arched eyebrow dimensions and spatial anchors
            brow_thick = max(4, width // 6)
            brow_width = int(width * 1.4)
            brow_height = int(width)

            # Arc bounding box hovering right over the right eye
            arc_rect = pygame.Rect(
                int(x - brow_width // 2),
                int(y - height // 2 - brow_height // 2 - 15),
                brow_width,
                brow_height,
            )

            # Top semicircle arc (0 to pi radians) for a smooth raised brow
            pygame.draw.arc(surface, color, arc_rect, 0, 3.14159, brow_thick)

        # Toggle state for the engine's next draw call
        self.drawing_left = not self.drawing_left
