import os
import pygame

# Obtém o caminho absoluto do diretório raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Caminho para a pasta de imagens
IMAGES_DIR = os.path.join(BASE_DIR, "src", "resources", "images")

# Configurações da Tela
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FPS = 60  # Adicionando FPS para controle do jogo

# Inicia o Pygame e define a tela temporariamente
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Necessário para carregar imagens corretamente


# Função para carregar imagens com transparência
def load_image(filename):
    return pygame.image.load(os.path.join(IMAGES_DIR, filename)).convert_alpha()


# Carrega Imagens
BIRD_IMAGES = [pygame.transform.scale2x(load_image(f'bird{i}.png')) for i in range(1, 4)]
PIPE_IMAGE = pygame.transform.scale2x(load_image('pipe.png'))
GROUND_IMAGE = pygame.transform.scale2x(load_image('base.png'))
BACKGROUND_IMAGE = pygame.transform.scale2x(load_image('bg.png'))

# Fonte do Jogo
SCORE_FONT = pygame.font.SysFont('arial', 50)
