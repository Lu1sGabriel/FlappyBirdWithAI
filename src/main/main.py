import pygame

from bird import Bird
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE, SCORE_FONT, FPS
from floor import Floor
from pipe import Pipe


def render_screen(screen, background, bird, pipes, floor, score):
    """Desenha todos os elementos na tela de forma otimizada."""
    screen.blit(background, (0, 0))

    for pipe in pipes:
        pipe.draw(screen)

    floor.draw(screen)
    bird.draw(screen)

    # Exibir pontuação
    score_text = SCORE_FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

    pygame.display.update()  # Atualiza apenas os elementos modificados


def run_game():
    """Loop principal do jogo."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    background = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bird = Bird(x=230, y=300)
    floor = Floor(y=SCREEN_HEIGHT - Floor.IMAGE.get_height())
    pipes = [Pipe(x=SCREEN_WIDTH + 200)]  # Adicionando apenas um cano no início
    score = 0
    running = True
    pipe_interval = 90  # Intervalo fixo entre os canos (frames)
    frames_since_last_pipe = 0

    while running:
        clock.tick(FPS)

        # Processamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Atualiza estado do jogo
        bird.move()
        floor.move()

        # Controle de geração de canos
        frames_since_last_pipe += 1
        if frames_since_last_pipe >= pipe_interval:
            pipes.append(Pipe(x=SCREEN_WIDTH + 100))  # Adiciona um novo cano a cada intervalo fixo
            frames_since_last_pipe = 0  # Reseta o contador

        # Gerenciar canos
        for pipe in pipes[:]:  # Iteração segura sobre a lista
            pipe.move()

            if not pipe.passed and bird.x > pipe.x:
                pipe.passed = True
                score += 1

            if pipe.check_collision(bird):
                running = False

            if pipe.x + pipe.top_pipe_image.get_width() < 0:
                pipes.remove(pipe)  # Remove canos fora da tela para evitar sobrecarga

        # Verifica colisão com o chão ou topo
        if bird.y + bird.current_image.get_height() >= floor.y or bird.y < 0:
            running = False

        # Renderiza o jogo
        render_screen(screen, background, bird, pipes, floor, score)

    pygame.quit()


if __name__ == "__main__":
    run_game()
