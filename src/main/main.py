import math
import os

import neat
import pygame

from bird import Bird
from config import BACKGROUND_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from floor import Floor
from pipe import Pipe

# Global Constants
AI_PLAYING = True
generation_count = 0

# Inicializa a fonte
pygame.font.init()
POINTS_FONT = pygame.font.SysFont('arial', 50)

def draw_background(screen):
    """Desenha o fundo para se ajustar à largura da tela."""
    background_width = BACKGROUND_IMAGE.get_width()
    for x in range(0, SCREEN_WIDTH, background_width):
        screen.blit(BACKGROUND_IMAGE, (x, 0))

def draw_game_screen(screen, birds, pipes, floor, points, generation):
    """Renderiza a tela do jogo com pássaros, canos, pontos e geração."""
    draw_background(screen)
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    points_text = POINTS_FONT.render(f"Points: {points}", True, (255, 255, 255))
    screen.blit(points_text, (SCREEN_WIDTH - 10 - points_text.get_width(), 10))

    if AI_PLAYING:
        generation_text = POINTS_FONT.render(f"Generation: {generation}", True, (255, 255, 255))
        screen.blit(generation_text, (10, 10))

    floor.draw(screen)
    pygame.display.update()

def process_events(birds):
    """Processa eventos do Pygame, como sair e entradas do teclado."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if not AI_PLAYING and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            for bird in birds:
                bird.jump()

def update_birds_and_genomes(birds, networks, genomes, pipes):
    """Atualiza a posição dos pássaros e suas respectivas redes neurais e genomas."""
    for i, bird in enumerate(birds):
        bird.move()
        genomes[i].fitness += 0.1  # Recompensa por permanecer vivo
        closest_pipe_index = get_closest_pipe_index(bird, pipes)
        bird_input_data = get_bird_input_data(bird, pipes[closest_pipe_index])
        bird_input_data += (bird.vertical_speed,)  # Adiciona a velocidade vertical aos dados de entrada
        output = networks[i].activate(bird_input_data)

        if sigmoid(output[0]) > 0.5:
            bird.jump()

def sigmoid(x):
    """Função de ativação sigmoide."""
    return 1 / (1 + math.exp(-x))

def get_closest_pipe_index(bird, pipes):
    """Retorna o índice do cano mais próximo do pássaro."""
    return 1 if pipes and bird.x > pipes[0].x + pipes[0].top_pipe_image.get_width() else 0

def get_bird_input_data(bird, pipe):
    """Retorna os dados de entrada para a rede neural do pássaro."""
    return (bird.y, abs(bird.y - pipe.height), abs(bird.y - pipe.bottom_y), pipe.height, pipe.bottom_y)

def initialize_genomes_and_birds(genomes, config):
    """Inicializa redes neurais, genomas e pássaros."""
    networks = []
    genome_list = []
    birds = []
    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        genome.fitness = 0
        genome_list.append(genome)
        birds.append(Bird(230, 350))
    return networks, genome_list, birds

def handle_bird_death(index, birds, genome_list, networks):
    """Lida com a morte do pássaro removendo-o e atualizando a aptidão."""
    birds.pop(index)
    if AI_PLAYING:
        genome_list[index].fitness -= 2  # Penalidade por colisão
        genome_list.pop(index)
        networks.pop(index)

def main(genomes, config):
    """Função principal do jogo gerenciando a lógica e a interação entre pássaros e canos."""
    global generation_count
    generation_count += 1

    networks, genome_list, birds = initialize_genomes_and_birds(genomes, config)

    floor = Floor(SCREEN_HEIGHT * 0.85)
    pipes = [Pipe(SCREEN_WIDTH)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    points = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        process_events(birds)

        if not birds:
            break  # Encerra se não houver pássaros restantes

        update_birds_and_genomes(birds, networks, genome_list, pipes)

        add_pipe = False
        remove_pipes = []

        for pipe in pipes:
            for i in range(len(birds) - 1, -1, -1):  # Itera de trás para frente
                if pipe.check_collision(birds[i]):
                    handle_bird_death(i, birds, genome_list, networks)
                elif not pipe.passed and birds[i].x > pipe.x:
                    pipe.passed = True
                    add_pipe = True

            pipe.move()
            if pipe.x + pipe.top_pipe_image.get_width() < 0:
                remove_pipes.append(pipe)

        if add_pipe:
            points += 1
            pipes.append(Pipe(SCREEN_WIDTH + 100))
            for genome in genome_list:
                genome.fitness += 6  # Recompensa por passar um cano

        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i in range(len(birds) - 1, -1, -1):  # Itera de trás para frente
            if birds[i].y + birds[i].rotated_image.get_height() > floor.y or birds[i].y < 0:
                handle_bird_death(i, birds, genome_list, networks)

        draw_game_screen(screen, birds, pipes, floor, points, generation_count)

def run(config_file):
    """Executa a configuração do NEAT e inicia a execução do jogo."""
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.run(main)

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    config_file_path = os.path.join(path, '..', 'resources', 'iaSettings', 'config.txt')
    run(config_file_path)
