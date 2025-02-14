import os
import pygame

# Obtém o caminho absoluto do diretório raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Caminho para a pasta de imagens e sons
IMAGES_DIR = os.path.join(BASE_DIR, "src", "resources", "images")
SOUNDS_DIR = os.path.join(BASE_DIR, "src", "resources", "sounds")

# Configurações da Tela
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FPS = 60  # Adicionando FPS para controle do jogo

def initialize_pygame():
    """Inicializa o Pygame e configura a tela."""
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    return screen

# Inicializa o Pygame e configura a tela
game_screen = initialize_pygame()

def load_image(filename):
    """Carrega uma imagem com transparência."""
    return pygame.image.load(os.path.join(IMAGES_DIR, filename)).convert_alpha()

def load_sound(filename, volume=0.5):
    """Carrega um arquivo de som com um volume especificado."""
    sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, filename))
    sound.set_volume(volume)
    return sound

def load_images():
    """Carrega todas as imagens necessárias para o jogo."""
    bird_images = [pygame.transform.scale2x(load_image(f'bird{i}.png')) for i in range(1, 4)]
    pipe_image = pygame.transform.scale2x(load_image('pipe.png'))
    ground_image = pygame.transform.scale2x(load_image('base.png'))
    background_image = pygame.transform.scale2x(load_image('bg.png'))
    return bird_images, pipe_image, ground_image, background_image

def load_sounds():
    """Carrega todos os sons necessários para o jogo."""
    flap_sound = load_sound('flap-101soundboards.mp3', volume=0.3)
    hit_sound = load_sound('flappy-bird-hit-sound-101soundboards.mp3', volume=0.3)
    point_sound = load_sound('point-101soundboards.mp3', volume=0.3)
    die_sound = load_sound('die-101soundboards.mp3', volume=0.3)
    return flap_sound, hit_sound, point_sound, die_sound

# Carrega as imagens e sons
BIRD_IMAGES, PIPE_IMAGE, GROUND_IMAGE, BACKGROUND_IMAGE = load_images()
FLAP_SOUND, HIT_SOUND, POINT_SOUND, DIE_SOUND = load_sounds()

# Fonte do Jogo
SCORE_FONT = pygame.font.SysFont('arial', 50)
