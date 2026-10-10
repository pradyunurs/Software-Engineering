
import random
import pygame


class Anvil:
    def __init__(self, screen_width):
        self.screen_width = screen_width

        self.width = 40
        self.height = 32

        # Spawn at a random horizontal position.
        self.x = random.randint(
            20,
            screen_width - self.width - 20
        )

        # Start just above the visible screen.
        self.y = -self.height

        # Each anvil has a randomized falling speed.
        self.speed = random.uniform(4.5, 7.0)

    def update(self):
        self.y += self.speed

    def is_off_screen(self, screen_height):
        return self.y > screen_height + 10

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def render(self, surface):
        # Select warning colors based on falling speed.
        if self.speed >= 6.5:
            top_color = (255, 70, 50)
            base_color = (170, 40, 40)

        elif self.speed >= 5.5:
            top_color = (255, 155, 40)
            base_color = (180, 95, 30)

        else:
            top_color = (120, 120, 130)
            base_color = (80, 80, 90)

        # Draw the upper part of the anvil.
        top_rect = pygame.Rect(
            int(self.x) + 4,
            int(self.y),
            self.width - 8,
            14
        )

        pygame.draw.rect(
            surface,
            top_color,
            top_rect,
            border_radius=2
        )

        # Draw the main body of the anvil.
        base_rect = pygame.Rect(
            int(self.x),
            int(self.y) + 14,
            self.width,
            18
        )

        pygame.draw.rect(
            surface,
            base_color,
            base_rect,
            border_radius=3
        )

        # Draw an outline.
        pygame.draw.rect(
            surface,
            (200, 200, 210),
            base_rect,
            width=1,
            border_radius=3
        )
