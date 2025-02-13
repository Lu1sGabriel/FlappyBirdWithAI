import pygame
from config import GROUND_IMAGE
from pipe import Pipe


class Floor:
    """Classe responsável pelo chão em movimento do jogo."""

    SCROLL_SPEED = Pipe.PIPE_MOVEMENT_SPEED  # Usa a mesma velocidade dos canos
    IMAGE: pygame.Surface = GROUND_IMAGE
    WIDTH: int = IMAGE.get_width()

    def __init__(self, y_position: int):
        """Inicializa a posição do chão."""
        self.y_position = y_position
        self.first_section_x = 0
        self.second_section_x = self.WIDTH

    def move(self):
        """Move o chão para a esquerda, criando um efeito de rolagem contínua."""
        self.first_section_x -= self.SCROLL_SPEED
        self.second_section_x -= self.SCROLL_SPEED

        # Se uma seção sair completamente da tela, reposicionamos para manter o loop infinito
        if self.first_section_x + self.WIDTH < 0:
            self.first_section_x = self.second_section_x + self.WIDTH

        if self.second_section_x + self.WIDTH < 0:
            self.second_section_x = self.first_section_x + self.WIDTH

    def draw(self, screen: pygame.Surface):
        """Desenha as duas seções do chão na tela."""
        screen.blit(self.IMAGE, (self.first_section_x, self.y_position))
        screen.blit(self.IMAGE, (self.second_section_x, self.y_position))
