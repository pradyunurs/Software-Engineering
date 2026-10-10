
import random
import pygame

from game.player import Player
from game.anvil import Anvil


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.player = Player(width, height)
        self.anvils = []
        self.particles = []

        # Difficulty settings.
        self.initial_spawn_delay = 700
        self.minimum_spawn_delay = 200
        self.spawn_delay = self.initial_spawn_delay

        self.last_spawn_time = pygame.time.get_ticks()
        self.start_ticks = pygame.time.get_ticks()

        self.survival_time = 0
        self.game_state = "PLAYING"

        # Fonts for the interface.
        self.font_big = pygame.font.SysFont(None, 52)
        self.font_medium = pygame.font.SysFont(None, 34)
        self.font_small = pygame.font.SysFont(None, 24)

    def handle_event(self, event):
        # Restart only when the game is over.
        if self.game_state == "GAME_OVER":
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                self.reset()

    def update(self):
        # Do not update gameplay after game over.
        if self.game_state != "PLAYING":
            return

        # Read the current keyboard state.
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()

        # Apply movement and boundary restrictions.
        self.player.update()

        # Calculate survival time in seconds.
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        self.survival_time = elapsed_ms // 1000

        # Increase difficulty over time by spawning anvils
        # more frequently, without going below 200 milliseconds.
        self.spawn_delay = max(
            self.minimum_spawn_delay,
            self.initial_spawn_delay - self.survival_time * 20
        )

        # Spawn a new anvil when the interval has elapsed.
        now = pygame.time.get_ticks()

        if now - self.last_spawn_time >= self.spawn_delay:
            self.anvils.append(Anvil(self.width))
            self.last_spawn_time = now

        # The ground is the horizontal line above the bottom bar.
        ground_y = self.height - 20
        player_rect = self.player.rect

        # Iterate over a copy so anvils can be safely removed.
        for anvil in self.anvils[:]:
            anvil.update()

            # Check collision before processing ground impact.
            if player_rect.colliderect(anvil.rect):
                self.game_state = "GAME_OVER"
                return

            # Produce an impact effect when an anvil hits
            # the ground, then remove the anvil.
            if anvil.rect.bottom >= ground_y:
                self.create_impact_effect(
                    anvil.x + anvil.width / 2,
                    ground_y
                )

                self.anvils.remove(anvil)
                continue

            # Extra cleanup for anvils that travel off-screen.
            if anvil.is_off_screen(self.height):
                self.anvils.remove(anvil)

        # Update the dust particles already on the screen.
        for particle in self.particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]

            # Gravity gradually pulls particles downward.
            particle["vy"] += 0.15
            particle["life"] -= 1

            if particle["life"] <= 0:
                self.particles.remove(particle)

    def create_impact_effect(self, x, y):
        # Generate a small dust cloud at the impact position.
        for _ in range(12):
            self.particles.append({
                "x": float(x),
                "y": float(y),
                "vx": random.uniform(-2.5, 2.5),
                "vy": random.uniform(-4.0, -1.0),
                "life": 20,
                "radius": random.randint(2, 4),
            })

    def reset(self):
        # Create a fresh player and clear old objects.
        self.player = Player(self.width, self.height)
        self.anvils.clear()
        self.particles.clear()

        # Reset the survival timer and spawn schedule.
        now = pygame.time.get_ticks()

        self.start_ticks = now
        self.last_spawn_time = now

        self.survival_time = 0
        self.spawn_delay = self.initial_spawn_delay

        # Return to normal gameplay.
        self.game_state = "PLAYING"

    def render(self, screen):
        # Draw the background.
        screen.fill((35, 38, 45))

        # Draw the ground.
        ground_y = self.height - 20

        pygame.draw.rect(
            screen,
            (70, 75, 85),
            (0, ground_y, self.width, 20)
        )

        pygame.draw.line(
            screen,
            (160, 90, 40),
            (0, ground_y),
            (self.width, ground_y),
            3
        )

        # Draw the player.
        self.player.render(screen)

        # Draw every falling anvil.
        for anvil in self.anvils:
            anvil.render(screen)

        # Draw ground-impact particles.
        for particle in self.particles:
            pygame.draw.circle(
                screen,
                (190, 175, 145),
                (
                    int(particle["x"]),
                    int(particle["y"])
                ),
                particle["radius"]
            )

        # Draw the survival timer.
        time_surf = self.font_medium.render(
            f"Survival Time: {self.survival_time}s",
            True,
            (240, 240, 240)
        )

        screen.blit(time_surf, (20, 20))

        # Draw the keyboard instructions.
        inst_surf = self.font_small.render(
            "Use [A/D] or [Arrow Keys] to Dodge",
            True,
            (170, 175, 185)
        )

        screen.blit(
            inst_surf,
            (
                self.width - inst_surf.get_width() - 20,
                25
            )
        )

        # Draw the game-over overlay.
        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render(
                "CRUSHED! GAME OVER",
                True,
                (235, 65, 65)
            )

            screen.blit(
                over_surf,
                (
                    self.width // 2 - over_surf.get_width() // 2,
                    self.height // 2 - 60
                )
            )

            score_surf = self.font_medium.render(
                f"You survived: {self.survival_time} seconds",
                True,
                (255, 255, 255)
            )

            screen.blit(
                score_surf,
                (
                    self.width // 2 - score_surf.get_width() // 2,
                    self.height // 2
                )
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again",
                True,
                (200, 200, 200)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 50
                )
            )
