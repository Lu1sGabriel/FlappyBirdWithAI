import pygame

from config import GROUND_IMAGE
from constants import PIPE_SPEED


class Floor:
    """Representa o chão do jogo.

    A classe Floor gerencia a movimentação e o desenho do chão na tela,
    permitindo um efeito contínuo de movimento.
    """

    SPEED = PIPE_SPEED
    IMAGE = GROUND_IMAGE
    WIDTH = IMAGE.get_width()

    def __init__(self, y: int):
        """Inicializa o chão na posição vertical especificada.

        Args:
            y: A coordenada vertical do chão na tela.
        """
        self.y = y
        self.x_positions = [0, self.WIDTH]

    def move(self):
        """Move o chão para a esquerda, criando um loop contínuo.

        Atualiza as posições horizontais do chão conforme a velocidade definida.
        Quando o chão sai da tela, seu posicionamento é ajustado para criar um efeito de looping.
        """
        self.x_positions = [x - self.SPEED for x in self.x_positions]
        self.reset_position_if_needed()

    def reset_position_if_needed(self):
        """Reposiciona a imagem que saiu da tela.

        Verifica se alguma parte do chão saiu da tela e, se necessário,
        reposiciona essa parte para criar um efeito contínuo de movimento.
        """
        for i in range(len(self.x_positions)):
            if self.x_positions[i] <= -self.WIDTH:
                self.x_positions[i] = self.WIDTH - self.SPEED

    def draw(self, screen: pygame.Surface):
        """Desenha o chão na tela.

        Renderiza a imagem do chão em suas posições atuais
        na superfície fornecida.

        Args:
            screen: A superfície onde o chão será desenhado.
        """
        for x in self.x_positions:
            screen.blit(self.IMAGE, (x, self.y))
