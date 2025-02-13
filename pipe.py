import pygame
import random
from config import PIPE_IMAGE
from bird import Bird


class Pipe:
    """Classe que representa os canos no jogo Flappy Bird."""

    GAP_BETWEEN_PIPES = 200  # Distância vertical entre os canos
    PIPE_MOVEMENT_SPEED = 5  # Velocidade com que os canos se movem para a esquerda
    MIN_PIPE_HEIGHT = 50
    MAX_PIPE_HEIGHT = 450

    def __init__(self, initial_x: int):
        """Inicializa um par de canos na posição X especificada."""
        self.x_position = initial_x
        self.pipe_height = 0
        self.top_pipe_y = 0
        self.bottom_pipe_y = 0
        self.top_pipe_image = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.bottom_pipe_image = PIPE_IMAGE
        self.has_passed = False  # Indica se o pássaro já passou pelo cano

        self._set_random_pipe_height()

    def _set_random_pipe_height(self):
        """Define uma altura aleatória para os canos, garantindo um espaço jogável."""
        self.pipe_height = random.randint(self.MIN_PIPE_HEIGHT, self.MAX_PIPE_HEIGHT)
        self.top_pipe_y = self.pipe_height - self.top_pipe_image.get_height()
        self.bottom_pipe_y = self.pipe_height + self.GAP_BETWEEN_PIPES

    def move(self):
        """Move os canos para a esquerda, simulando o deslocamento do jogo."""
        self.x_position -= self.PIPE_MOVEMENT_SPEED

    def draw(self, screen: pygame.Surface):
        """Desenha os canos na tela."""
        screen.blit(self.top_pipe_image, (self.x_position, self.top_pipe_y))
        screen.blit(self.bottom_pipe_image, (self.x_position, self.bottom_pipe_y))

    def check_collision(self, bird: Bird) -> bool:
        """Verifica se o pássaro colidiu com um dos canos."""
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.top_pipe_image)
        bottom_pipe_mask = pygame.mask.from_surface(self.bottom_pipe_image)

        top_offset = (self.x_position - bird.x_position, self.top_pipe_y - bird.y_position)
        bottom_offset = (self.x_position - bird.x_position, self.bottom_pipe_y - bird.y_position)

        top_collision = bird_mask.overlap(top_pipe_mask, top_offset)
        bottom_collision = bird_mask.overlap(bottom_pipe_mask, bottom_offset)

        return bool(top_collision) or bool(bottom_collision)
