import random
import sys

import pygame

from core.manager import StateManager
from settings import *


class FaceEngine:
    def __init__(self, states=None):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)

        self.screen = pygame.display.set_mode((0, 0))
        self.width, self.height = self.screen.get_size()
        self.center_x, self.center_y = self.width // 2, self.height // 2
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        total_eyes_width = (EYE_WIDTH * 2) + EYE_GAP
        self.max_move_x = max(
            0, (self.width - total_eyes_width) // 2 - SCREEN_PADDING_X
        )
        self.max_move_y = max(0, (self.height - EYE_HEIGHT) // 2 - SCREEN_PADDING_Y)

        # The engine only tracks the active name, not the instances
        self.active_expression_name = "normal"
        self.default_expression = "normal"
        self.expression_timer_end = 0

        self.state_manager = StateManager()
        if states:
            for state in states:
                self.state_manager.register_state(state)

        self.current_x, self.current_y = 0.0, 0.0
        self.target_x, self.target_y = 0.0, 0.0

        self.next_look_time = pygame.time.get_ticks() + 1000
        self.next_blink_time = pygame.time.get_ticks() + 4500
        self.is_blinking = False
        self.blink_start_time = 0

    def trigger_expression(self, name, context):
        """Helper to switch expressions based on context data."""
        if name in context.expressions:
            self.active_expression_name = name
            duration = context.expressions[name]["duration_ms"]
            if duration > 0:
                self.expression_timer_end = pygame.time.get_ticks() + duration
            else:
                self.expression_timer_end = 0

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()

            # All expressions and states are injected here
            context = self.state_manager.resolve(current_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    running = False

            # Revert Expression Timer
            if (
                self.expression_timer_end > 0
                and current_time > self.expression_timer_end
            ):
                self.active_expression_name = self.default_expression
                self.expression_timer_end = 0

            # Blinking Logic
            if (
                context.expression_override is None
                and self.active_expression_name == self.default_expression
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
                self.target_x = (
                    random.randint(-self.max_move_x, self.max_move_x)
                    * context.movement_multiplier
                )
                self.target_y = (
                    random.randint(-self.max_move_y, self.max_move_y)
                    * context.movement_multiplier
                )

                # Iterate through whatever expressions the states injected this frame
                for name, data in context.expressions.items():
                    if (
                        name != self.default_expression
                        and data["chance"] > 0
                        and random.random() < data["chance"]
                    ):
                        self.trigger_expression(name, context)
                        break

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

            # Determine target expression from Context
            target_name = context.expression_override or self.active_expression_name
            expression_data = context.expressions.get(target_name)

            if expression_data and expression_data["instance"]:
                expr = expression_data["instance"]
                expr.draw_eye(
                    self.screen,
                    left_x,
                    base_y,
                    EYE_WIDTH,
                    current_eye_height,
                    context.color,
                )
                expr.draw_eye(
                    self.screen,
                    right_x,
                    base_y,
                    EYE_WIDTH,
                    current_eye_height,
                    context.color,
                )

            # Render Artifacts
            for artifact in context.artifacts:
                if artifact["type"] == "text":
                    text_surface = self.font.render(
                        artifact["text"], True, artifact.get("color", (255, 255, 255))
                    )
                    self.screen.blit(
                        text_surface, (artifact.get("x", 0), artifact.get("y", 0))
                    )

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
