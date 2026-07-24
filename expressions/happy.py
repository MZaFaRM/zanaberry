import pygame

from expressions.base import Expression


class Happy(Expression):
    def draw_eye(self, surface, x, y, width, height, color):
        rect = pygame.Rect(int(x - width // 2), int(y - height // 2 + 40), width, width)
        pygame.draw.arc(surface, color, rect, 0, 3.14159, 15)