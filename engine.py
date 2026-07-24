# engine.py
import random
import sys

import pygame

from settings import *


class FaceEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        self.center_x, self.center_y = self.width // 2, self.height // 2
        pygame.display.set_caption("Z.AI Face Engine")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        total_eyes_width = (EYE_WIDTH * 2) + EYE_GAP

        self.max_move_x = max(
            0, (self.width - total_eyes_width) // 2 - SCREEN_PADDING_X
        )
        self.max_move_y = max(0, (self.height - EYE_HEIGHT) // 2 - SCREEN_PADDING_Y)

        # Expression State Management
        self.expressions = {}
        self.current_expression = None
        self.default_expression = "normal"
        self.expression_timer_end = 0

        # Physics State
        self.current_x, self.current_y = 0.0, 0.0
        self.target_x, self.target_y = 0.0, 0.0

        # Timers
        self.next_look_time = pygame.time.get_ticks() + 1000
        self.next_blink_time = pygame.time.get_ticks() + 4500
        self.is_blinking = False
        self.blink_start_time = 0

    def register_expression(self, name, expression_instance):
        """Registers a new expression module to the engine."""
        self.expressions[name] = expression_instance
        if self.current_expression is None:
            self.set_expression(name)

    def set_expression(self, name, duration_ms=0):
        """Switches the face to a named expression. Reverts to default if duration_ms > 0."""
        if name in self.expressions:
            self.current_expression = self.expressions[name]
            if duration_ms > 0:
                self.expression_timer_end = pygame.time.get_ticks() + duration_ms
            else:
                self.expression_timer_end = 0

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # Revert Expression Timer
            if (
                self.expression_timer_end > 0
                and current_time > self.expression_timer_end
            ):
                self.set_expression(self.default_expression)

            # Blinking Logic
            # (Only blink if we are in the normal state)
            if (
                self.current_expression == self.expressions.get(self.default_expression)
                and not self.is_blinking
                and current_time > self.next_blink_time
            ):
                self.is_blinking = True
                self.blink_start_time = current_time
                self.next_blink_time = current_time + random.randint(3000, 5000)

            current_eye_height = EYE_HEIGHT
            if self.is_blinking:
                elapsed = current_time - self.blink_start_time
                if elapsed < 50:
                    current_eye_height = max(
                        10, EYE_HEIGHT - (EYE_HEIGHT * (elapsed / 50))
                    )
                elif elapsed < 100:
                    current_eye_height = min(
                        EYE_HEIGHT, 10 + (EYE_HEIGHT * ((elapsed - 50) / 50))
                    )
                else:
                    self.is_blinking = False
                    current_eye_height = EYE_HEIGHT

            # Idle Movement & Random Behaviors
            if current_time > self.next_look_time:
                self.target_x = random.randint(-self.max_move_x, self.max_move_x)
                self.target_y = random.randint(-self.max_move_y, self.max_move_y)

                # 25% chance to do a happy squint
                if random.random() > 0.75:
                    self.set_expression("happy", duration_ms=1500)

                # 30% chance to reset to center
                if random.random() > 0.7:
                    self.target_x, self.target_y = 0, 0

                self.next_look_time = current_time + random.randint(1000, 3500)

            # Physics
            self.current_x += (self.target_x - self.current_x) * SMOOTHING_SPEED
            self.current_y += (self.target_y - self.current_y) * SMOOTHING_SPEED

            # Render
            self.screen.fill(BLACK)

            left_x = self.center_x - (EYE_WIDTH // 2) - (EYE_GAP // 2) + self.current_x
            right_x = self.center_x + (EYE_WIDTH // 2) + (EYE_GAP // 2) + self.current_x
            base_y = self.center_y + self.current_y

            # Draw the active expression
            if self.current_expression:
                self.current_expression.draw_eye(
                    self.screen, left_x, base_y, EYE_WIDTH, current_eye_height, CYAN
                )
                self.current_expression.draw_eye(
                    self.screen, right_x, base_y, EYE_WIDTH, current_eye_height, CYAN
                )

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
