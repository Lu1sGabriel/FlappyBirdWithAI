import random
import pygame
from bird import Bird
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE, SCORE_FONT, FPS, FLAP_SOUND, HIT_SOUND, POINT_SOUND, DIE_SOUND
from floor import Floor
from pipe import Pipe

def render_screen(screen, background, bird, pipes, floor, score):
    """Desenha todos os elementos na tela de forma otimizada."""
    screen.blit(background, (0, 0))
    for pipe in pipes:
        pipe.draw(screen)
    floor.draw(screen)
    bird.draw(screen)
    score_text = SCORE_FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
    pygame.display.update()

def process_events(bird, game_started):
    """Processa os eventos do jogo."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, game_started
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()
            FLAP_SOUND.play()  # Reproduz o som de pulo
            game_started = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bird.jump()
            FLAP_SOUND.play()  # Reproduz o som de pulo
            game_started = True
    return True, game_started

def generate_new_pipe(pipes):
    """Gera um novo cano com variação de altura aleatória."""
    min_pipe_height = 50  # Altura mínima do cano
    max_pipe_height = SCREEN_HEIGHT - Floor.IMAGE.get_height() - Pipe.GAP - 50  # Altura máxima do cano
    new_pipe_height = random.randint(min_pipe_height, max_pipe_height)
    new_pipe = Pipe(x=SCREEN_WIDTH + 100)
    new_pipe.height = new_pipe_height
    new_pipe.top_y = new_pipe.height - new_pipe.pipe_height
    new_pipe.bottom_y = new_pipe.height + new_pipe.GAP
    pipes.append(new_pipe)

def update_game_state(bird, floor, pipes, score, frames_since_last_pipe, pipe_interval, game_started):
    """Atualiza o estado do jogo."""
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
                POINT_SOUND.play()  # Reproduz o som de ponto
            if pipe.check_collision(bird):
                HIT_SOUND.play()  # Reproduz o som de colisão
                DIE_SOUND.play()  # Reproduz o som de morte
                bird.collided = True
            if pipe.x + pipe.top_pipe_image.get_width() < 0:
                pipes_to_remove.append(pipe)

        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        if bird.y + bird.current_image.get_height() >= floor.y or bird.y < 0:
            HIT_SOUND.play()  # Reproduz o som de colisão
            DIE_SOUND.play()  # Reproduz o som de morte
            bird.collided = True

    return True, score, frames_since_last_pipe

def initialize_game():
    """Inicializa o jogo e retorna os objetos principais."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    background = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return screen, clock, background

def create_game_objects():
    """Cria os objetos principais do jogo."""
    bird = Bird(x=230, y=300)
    floor = Floor(y=SCREEN_HEIGHT - Floor.IMAGE.get_height())
    pipes = []
    return bird, floor, pipes

def handle_collision(screen, background, bird, pipes, floor, score):
    """Trata a queda do pássaro após a colisão."""
    while bird.y + bird.current_image.get_height() < floor.y:
        bird.y += 5  # Aumenta a velocidade de queda para um efeito mais rápido
        bird.angle = -90  # Faz o pássaro cair de cabeça para baixo
        bird.update_animation()
        render_screen(screen, background, bird, pipes, floor, score)
        pygame.time.delay(10)
    HIT_SOUND.play()  # Reproduz o som de colisão ao bater no chão
    DIE_SOUND.play()  # Reproduz o som de morte ao bater no chão

def run_game():
    """Loop principal do jogo."""
    screen, clock, background = initialize_game()
    bird, floor, pipes = create_game_objects()
    score = 0
    running = True
    game_started = False
    pipe_interval = 70  # Intervalo reduzido entre os canos para aumentar a dificuldade
    frames_since_last_pipe = 0

    while running:
        clock.tick(FPS)
        running, game_started = process_events(bird, game_started)
        if not running:
            break

        if game_started:
            running, score, frames_since_last_pipe = update_game_state(bird, floor, pipes, score, frames_since_last_pipe, pipe_interval, game_started)
            if bird.collided:
                handle_collision(screen, background, bird, pipes, floor, score)
                running = False
        else:
            bird.update_animation()
            floor.move()

        render_screen(screen, background, bird, pipes, floor, score)

    pygame.quit()

if __name__ == "__main__":
    run_game()
