import pygame

from config import GROUND_IMAGE
from constants import PIPE_SPEED


class Floor:
    """Representa o chão em movimento no jogo."""

    SPEED = PIPE_SPEED  # Velocidade de movimento do chão
    IMAGE = GROUND_IMAGE
    WIDTH = IMAGE.get_width()

    def __init__(self, y: int):
        self.y = y
        self.x_positions = [0, self.WIDTH]  # Posições x das duas imagens do chão

    def move(self):
        """Move o chão para a esquerda, criando um loop contínuo."""
        self.x_positions = [x - self.SPEED for x in self.x_positions]

        # Reposiciona a imagem que saiu da tela para criar o efeito infinito
        for i in range(len(self.x_positions)):
            if self.x_positions[i] <= -self.WIDTH:
                self.x_positions[i] = self.WIDTH - self.SPEED

    def draw(self, screen: pygame.Surface):
        """Desenha o chão na tela."""
        for x in self.x_positions:
            screen.blit(self.IMAGE, (x, self.y))
