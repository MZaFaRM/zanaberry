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
        # pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        # The engine only tracks the active name, not the instances
        self.active_expression_name = "normal"
        self.default_expression = "normal"
        self.expression_timer_end = 0

        self.state_manager = StateManager()
        if states:
            for state in states:
                self.state_manager.register_state(state)

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

            current_eye_height = EYE_HEIGHT

            # Random Behaviors (Expressions only, movement removed)
            if current_time > self.next_look_time:
                # Iterate through whatever expressions the states injected this frame
                for name, data in context.expressions.items():
                    if (
                        name != self.default_expression
                        and data["chance"] > 0
                        and random.random() < data["chance"]
                    ):
                        self.trigger_expression(name, context)
                        break

                self.next_look_time = current_time + random.randint(1000, 3500)

            # Render
            self.screen.fill(BLACK)

            # Draw exactly in the center without current_x / current_y offsets
            left_x = self.center_x - (EYE_WIDTH // 2) - (EYE_GAP // 2)
            base_y = self.center_y

            # Determine target expression from Context
            target_name = context.expression_override or self.active_expression_name
            expression_data = context.expressions.get(target_name)

            if expression_data and expression_data["draw_fn"]:
                draw_func = expression_data["draw_fn"]
                draw_func(
                    self.screen,
                    left_x,
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
