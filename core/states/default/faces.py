import pygame

from core.states.base.faces import Face


class Normal(Face):
    def draw_eye(self, surface, x, y, width, height, color):
        rect = pygame.Rect(
            int(x - width // 2), int(y - height // 2), width, int(height)
        )
        pygame.draw.rect(surface, color, rect, border_radius=40)


class Happy(Face):
    def draw_eye(self, surface, x, y, width, height, color):
        rect = pygame.Rect(int(x - width // 2), int(y - height // 2 + 40), width, width)
        pygame.draw.arc(surface, color, rect, 0, 3.14159, 15)


class Curious(Face):
    def __init__(self):
        super().__init__()
        self.drawing_left = True

    def draw_eye(self, surface, x, y, width, height, color):
        if self.drawing_left:
            eye_height = max(10, height // 3)
            rect = pygame.Rect(
                int(x - width // 2), int(y - eye_height // 2), width, int(eye_height)
            )
            pygame.draw.rect(surface, color, rect, border_radius=40)
        else:
            rect = pygame.Rect(
                int(x - width // 2), int(y - height // 2 - 10), width, int(height)
            )
            pygame.draw.rect(surface, color, rect, border_radius=40)

            brow_thick = max(4, width // 6)
            brow_width = int(width * 1.4)
            brow_height = int(width)
            arc_rect = pygame.Rect(
                int(x - brow_width // 2),
                int(y - height // 2 - brow_height // 2 - 15),
                brow_width,
                brow_height,
            )
            pygame.draw.arc(surface, color, arc_rect, 0, 3.14159, brow_thick)

        self.drawing_left = not self.drawing_left