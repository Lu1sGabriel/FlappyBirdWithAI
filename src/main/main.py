import pygame

from bird import Bird
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE, SCORE_FONT, FPS
from floor import Floor
from pipe import Pipe


def render_screen(screen, bird, pipes, floor, score):
    """Desenha todos os elementos na tela."""
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(screen)

    floor.draw(screen)
    bird.draw(screen)

    # Exibir pontuação na tela
    score_text = SCORE_FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

    pygame.display.flip()  # Substitui pygame.display.update()


def run_game():
    """Loop principal do jogo."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird = Bird(x=230, y=300)
    floor = Floor(y=SCREEN_HEIGHT - Floor.IMAGE.get_height())
    pipes = [Pipe(x=700)]
    score = 0
    running = True

    while running:
        clock.tick(FPS)

        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Atualiza o estado do jogo
        bird.move()
        floor.move()

        add_new_pipe = False
        pipes_to_remove = []

        for pipe in pipes:
            pipe.move()

            # Verifica se o pássaro passou pelo cano
            if not pipe.passed and bird.x > pipe.x:
                pipe.passed = True
                add_new_pipe = True

            # Verifica colisão
            if pipe.check_collision(bird):
                running = False

            # Verifica se o cano saiu da tela
            if pipe.x + pipe.top_pipe_image.get_width() < 0:
                pipes_to_remove.append(pipe)

        if add_new_pipe:
            score += 1
            pipes.append(Pipe(x=SCREEN_WIDTH))

        # Remove canos que saíram da tela
        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        # Verifica se o pássaro tocou o chão ou saiu pela parte superior
        if bird.y + bird.current_image.get_height() >= floor.y or bird.y < 0:
            running = False

        # Renderiza a tela
        render_screen(screen, bird, pipes, floor, score)

    pygame.quit()


if __name__ == "__main__":
    run_game()
