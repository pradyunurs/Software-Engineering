
import pygame


class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.width = 44
        self.height = 54
        self.speed = 7

        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - self.height - 20

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def update(self):
        # Keep the entire player inside the screen.
        max_x = self.screen_width - self.width
        self.x = max(0, min(self.x, max_x))

        # Keep the player above the ground.
        ground_y = self.screen_height - 20
        max_y = ground_y - self.height
        self.y = max(0, min(self.y, max_y))

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def render(self, surface):
        # Draw the player's body.
        torso_rect = pygame.Rect(
            int(self.x) + 6,
            int(self.y) + 18,
            32,
            36
        )

        pygame.draw.rect(
            surface,
            (50, 130, 220),
            torso_rect,
            border_radius=4
        )

        # Draw the player's head.
        pygame.draw.circle(
            surface,
            (230, 200, 160),
            (int(self.x) + 22, int(self.y) + 12),
            12
        )

        # Draw the helmet.
        helmet_rect = pygame.Rect(
            int(self.x) + 8,
            int(self.y) - 2,
            28,
            12
        )

        pygame.draw.rect(
            surface,
            (180, 180, 190),
            helmet_rect,
            border_radius=4
        )
