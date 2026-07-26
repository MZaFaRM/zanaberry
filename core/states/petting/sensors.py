import pygame

from settings import FACE_HEIGHT, FACE_WIDTH

LAST_MOUSE_POS = (0, 0)
LAST_PET_TIME = 0
PET_COOLDOWN_MS = 750


def check_petting(current_time):
    global LAST_MOUSE_POS, LAST_PET_TIME

    screen = pygame.display.get_surface()
    if not screen:
        return False

    pet_x, pet_y = screen.get_rect().center

    face_width = FACE_WIDTH
    face_height = FACE_HEIGHT

    head_rect = pygame.Rect(
        pet_x - (face_width // 2),
        pet_y - (face_height // 2),
        face_width,
        face_height // 2,
    )

    mx, my = pygame.mouse.get_pos()

    if (head_rect.collidepoint(mx, my)) and ((mx, my) != LAST_MOUSE_POS):
        LAST_MOUSE_POS = (mx, my)
        LAST_PET_TIME = current_time

    return (current_time - LAST_PET_TIME) < PET_COOLDOWN_MS
