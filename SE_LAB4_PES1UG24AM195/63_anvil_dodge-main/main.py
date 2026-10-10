
import pygame

from game.game_engine import GameEngine


WIDTH, HEIGHT = 700, 500
FPS = 60


def main():
    pygame.init()

    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Anvil Dodge - Pygame Edition")

        clock = pygame.time.Clock()
        engine = GameEngine(WIDTH, HEIGHT)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    engine.handle_event(event)

            if not running:
                break

            engine.update()
            engine.render(screen)

            pygame.display.flip()
            clock.tick(FPS)

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
