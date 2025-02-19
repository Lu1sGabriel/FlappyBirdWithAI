import random

import pygame

from bird import Bird
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE, SCORE_FONT, FPS, FLAP_SOUND, HIT_SOUND, POINT_SOUND, \
    DIE_SOUND
from floor import Floor
from pipe import Pipe


def render_screen(screen, background, pipes, floor, score):
    """Desenha todos os elementos na tela de forma otimizada.

    Renderiza o fundo, os canos, o chão e o pássaro,
    além de exibir a pontuação atual no canto superior da tela.

    Args:
        screen: A superfície na qual os elementos do jogo serão desenhados.
        background: A imagem de fundo do jogo.
        pipes: Lista de instâncias de canos.
        floor: A instância do chão.
        score: A pontuação atual do jogador.
    """
    screen.blit(background, (0, 0))
    for pipe in pipes:
        pipe.draw(screen)
    floor.draw(screen)
    score_text = SCORE_FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
    pygame.display.update()


def process_events(bird, game_started):
    """Processa os eventos do jogo.

    Verifica os eventos de entrada do jogador, permitindo que
    o pássaro pule ao pressionar a tecla de espaço ou clicar com o mouse.

    Args:
        bird: A instância do pássaro.
        game_started: Um booleano indicando se o jogo já começou.

    Returns:
        Um tuple (running, game_started) onde running é um booleano
        que indica se o jogo deve continuar e game_started é atualizado.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, game_started
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()
            FLAP_SOUND.play()
            game_started = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bird.jump()
            FLAP_SOUND.play()
            game_started = True
    return True, game_started


def generate_new_pipe(pipes):
    """Gera um novo cano com variação de altura aleatória.

    Cria um novo cano e define sua altura dentro de limites
    específicos. O novo cano é então adicionado à lista de canos.

    Args:
        pipes: Lista de instâncias de canos existentes.
    """
    min_pipe_height = 50  # Altura mínima do cano
    max_pipe_height = SCREEN_HEIGHT - Floor.IMAGE.get_height() - Pipe.GAP - 50  # Altura máxima do cano
    new_pipe_height = random.randint(min_pipe_height, max_pipe_height)
    new_pipe = Pipe(x=SCREEN_WIDTH + 100)
    new_pipe.height = new_pipe_height
    new_pipe.top_y = new_pipe.height - new_pipe.pipe_height
    new_pipe.bottom_y = new_pipe.height + new_pipe.GAP
    pipes.append(new_pipe)


def update_game_state(bird, floor, pipes, score, frames_since_last_pipe, pipe_interval, game_started):
    """Atualiza o estado do jogo.

    Atualiza a posição do pássaro e do chão, verifica as colisões
    e faz a gerência da pontuação. Além disso, gera novos canos conforme necessário.

    Args:
        bird: A instância do pássaro.
        floor: A instância do chão.
        pipes: Lista de instâncias de canos.
        score: A pontuação atual do jogador.
        frames_since_last_pipe: O número de frames desde o último cano gerado.
        pipe_interval: O intervalo em frames para a geração de novos canos.
        game_started: Um booleano indicando se o jogo já começou.

    Returns:
        Um tuple (running, score, frames_since_last_pipe) onde running é um booleano
        que indica se o jogo deve continuar, score é a pontuação atualizada, e
        frames_since_last_pipe é atualizado.
    """
    if game_started:
        bird.move()
        floor.move()

        frames_since_last_pipe += 1
        if frames_since_last_pipe >= pipe_interval:
            generate_new_pipe(pipes)
            frames_since_last_pipe = 0

        pipes_to_remove = []
        for pipe in pipes:
            pipe.move()
            if not pipe.passed and bird.x > pipe.x:
                pipe.passed = True
                score += 1
                POINT_SOUND.play()
            if pipe.check_collision(bird):
                HIT_SOUND.play()
                DIE_SOUND.play()
                bird.collided = True
            if pipe.x + pipe.top_pipe_image.get_width() < 0:
                pipes_to_remove.append(pipe)

        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        if bird.y + bird.current_image.get_height() >= floor.y or bird.y < 0:
            HIT_SOUND.play()
            DIE_SOUND.play()
            bird.collided = True

    return True, score, frames_since_last_pipe


def initialize_game():
    """Inicializa o jogo e retorna os objetos principais.

    Configura o ambiente do jogo, incluindo a tela, o relógio
    e a imagem de fundo. Retorna a superfície da tela, o objeto do relógio e a imagem de fundo.

    Returns:
        Um tuple (screen, clock, background) contendo a superfície da tela,
        o relógio do jogo e a imagem de fundo.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    background = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return screen, clock, background


def create_game_objects():
    """Cria os objetos principais do jogo.

    Instancia o pássaro, o chão e a lista de canos, retornando-os
    como uma tupla.

    Returns:
        Um tuple (bird, floor, pipes) contendo a instância do pássaro,
        a instância do chão e a lista de canos.
    """
    bird = Bird(x=230, y=300)
    floor = Floor(y=SCREEN_HEIGHT - Floor.IMAGE.get_height())
    pipes = []
    return bird, floor, pipes


def handle_collision(screen, background, bird, pipes, floor, score):
    """Trata a queda do pássaro após a colisão.

    Faz com que o pássaro caia até o chão após uma colisão, além
    de reproduzir os sons de colisão e morte.

    Args:
        screen: A superfície na qual os elementos do jogo serão desenhados.
        background: A imagem de fundo do jogo.
        bird: A instância do pássaro.
        pipes: Lista de instâncias de canos.
        floor: A instância do chão.
        score: A pontuação atual do jogador.
    """
    while bird.y + bird.current_image.get_height() < floor.y:
        bird.y += 5
        bird.angle = -90
        bird.update_animation()
        render_screen(screen, background, pipes, floor, score)
        pygame.time.delay(10)
    HIT_SOUND.play()
    DIE_SOUND.play()


def run_game():
    """Loop principal do jogo.

    Gerencia o ciclo do jogo, processando eventos, atualizando o estado
    do jogo e renderizando a tela até que o jogo seja encerrado.

    O ciclo do jogo continua enquanto o jogador não fechar a janela.
    """
    screen, clock, background = initialize_game()
    bird, floor, pipes = create_game_objects()
    score = 0
    running = True
    game_started = False
    pipe_interval = 70
    frames_since_last_pipe = 0

    while running:
        clock.tick(FPS)
        running, game_started = process_events(bird, game_started)
        if not running:
            break

        if game_started:
            running, score, frames_since_last_pipe = update_game_state(bird, floor, pipes, score,
                                                                       frames_since_last_pipe, pipe_interval,
                                                                       game_started)
            if bird.collided:
                handle_collision(screen, background, bird, pipes, floor, score)
                running = False
        else:
            bird.update_animation()
            floor.move()

        render_screen(screen, background, pipes, floor, score)

    pygame.quit()


if __name__ == "__main__":
    run_game()
