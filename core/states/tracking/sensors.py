import pygame

LAST_MOUSE_POS = (0, 0)
LAST_MOVE_TIME = 0

COOLDOWN_MS = 750


def check_mouse_moving(current_time):
    global LAST_MOUSE_POS, LAST_MOVE_TIME

    current_pos = pygame.mouse.get_pos()

    if current_pos != LAST_MOUSE_POS:
        LAST_MOUSE_POS = current_pos
        LAST_MOVE_TIME = current_time

    return (current_time - LAST_MOVE_TIME) < COOLDOWN_MS
