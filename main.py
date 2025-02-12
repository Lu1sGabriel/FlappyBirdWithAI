import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE, SCORE_FONT
from bird import Bird

# Inicializa o Pygame
pygame.init()

# Configura a tela
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")


def render_screen(screen, bird, current_score):
    """Desenha todos os elementos na tela."""
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    bird.draw(screen)

    # Exibir pontuação na tela
    score_display = SCORE_FONT.render(f"Score: {current_score}", True, (255, 255, 255))
    screen.blit(score_display, (SCREEN_WIDTH - score_display.get_width() - 10, 10))

    pygame.display.update()


def run_game():
    """Loop principal do jogo."""
    game_clock = pygame.time.Clock()
    bird = Bird(start_x=230, start_y=350)
    current_score = 0
    game_running = True

    while game_running:
        game_clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.move()
        render_screen(game_screen, bird, current_score)

    pygame.quit()


if __name__ == "__main__":
    run_game()
