import os

import pygame

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

IMAGES_DIR = os.path.join(BASE_DIR, "src", "resources", "images")

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 900
FPS = 60


def initialize_pygame():
    """Inicializa o Pygame e configura a tela.

    Inicializa o Pygame, configura a tela com as dimensões
    especificadas e define o título da janela do jogo.

    Returns:
        screen: A superfície da tela onde o jogo será renderizado.
    """
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    return screen


# Inicializa o Pygame e configura a tela
game_screen = initialize_pygame()


def load_image(filename):
    """Carrega uma imagem com transparência.

    Args:
        filename: O nome do arquivo da imagem a ser carregada.

    Returns:
        A imagem carregada com suporte a transparência.
    """
    return pygame.image.load(os.path.join(IMAGES_DIR, filename)).convert_alpha()


def load_images():
    """Carrega todas as imagens necessárias para o jogo.

    Retorna uma lista de imagens de pássaros, a imagem do cano, a imagem
    do chão e a imagem de fundo.

    Returns:
        tuple: Uma tupla contendo as imagens do pássaro, cano, chão e fundo.
    """
    bird_images = [pygame.transform.scale2x(load_image(f'bird{i}.png')) for i in range(1, 4)]
    pipe_image = pygame.transform.scale2x(load_image('pipe.png'))
    ground_image = pygame.transform.scale2x(load_image('base.png'))
    background_image = pygame.transform.scale2x(load_image('bg.png'))
    return bird_images, pipe_image, ground_image, background_image


# Carrega as imagens e sons
BIRD_IMAGES, PIPE_IMAGE, GROUND_IMAGE, BACKGROUND_IMAGE = load_images()

# Fonte do Jogo
SCORE_FONT = pygame.font.SysFont('arial', 50)
