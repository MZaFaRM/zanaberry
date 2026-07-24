import pygame

from expressions.base import Expression


class Normal(Expression):
    def draw_eye(self, surface, x, y, width, height, color):
        rect = pygame.Rect(
            int(x - width // 2), int(y - height // 2), width, int(height)
        )
        pygame.draw.rect(surface, color, rect, border_radius=40)
