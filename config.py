import pygame
import os

# Configurações da Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# Carregar Imagens
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
GROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))

BIRD_FRAMES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png')))
]

# Fonte do Jogo
pygame.font.init()
SCORE_FONT = pygame.font.SysFont('arial', 50)
