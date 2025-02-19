import random

import pygame

from config import PIPE_IMAGE, SCREEN_HEIGHT
from constants import PIPE_SPEED
from floor import Floor


class Pipe(pygame.sprite.Sprite):
    """Representa os canos do jogo Flappy Bird.

    A classe Pipe gerencia a criação, movimento e colisão dos canos que o pássaro deve evitar.
    Os canos têm uma altura variável e se movem para a esquerda na tela.
    """

    SPEED = PIPE_SPEED
    GAP = 140

    def __init__(self, x: int):
        """Inicializa uma nova instância de Pipe.

        Args:
            x (int): A posição inicial do cano no eixo x.
        """
        super().__init__()
        self.x = x
        self.passed = False

        self.pipe_image = PIPE_IMAGE
        self.top_pipe_image = pygame.transform.flip(self.pipe_image, False, True)
        self.bottom_pipe_image = self.pipe_image

        self._initialize_dimensions()
        self._generate_heights()
        self._setup_rects()
        self._calculate_masks()

    def _initialize_dimensions(self):
        """Inicializa as dimensões do cano com base na tela e no chão.

        Calcula a altura mínima e máxima dos canos, garantindo
        que eles não se sobreponham ao chão e respeitem a distância do GAP.
        """
        ground_height = Floor.IMAGE.get_height()
        ground_level = SCREEN_HEIGHT - ground_height

        pipe_height = self.pipe_image.get_height()
        min_height = pipe_height // 7
        max_height = max(min_height + 80, ground_level - self.GAP - min_height)  # Aumentada a diferença

        self.pipe_height = pipe_height
        self.min_height = min_height
        self.max_height = max_height

    def _generate_heights(self):
        """Gera as alturas dos canos superior e inferior com maior variação.

        As alturas dos canos são geradas aleatoriamente dentro dos limites
        definidos, e uma aleatoriedade extra pode ser adicionada para
        diversificar a dificuldade do jogo.
        """
        self.height = random.randint(self.min_height, self.max_height)
        if random.random() < 0.7:
            self.height += random.randint(-40, 40)
        self.top_y = self.height - self.pipe_height
        self.bottom_y = self.height + self.GAP

    def _setup_rects(self):
        """Configura os retângulos de colisão dos canos.

        Define os retângulos de colisão para os canos superior e inferior
        com base nas suas respectivas posições na tela.
        """
        self.top_rect = self.top_pipe_image.get_rect(x=self.x, y=self.top_y)
        self.bottom_rect = self.bottom_pipe_image.get_rect(x=self.x, y=self.bottom_y)

    def _calculate_masks(self):
        """Gera as máscaras de colisão dos canos.

        As máscaras de colisão são usadas para verificar se houve colisões
        entre os canos e outros sprites, como o pássaro.
        """
        self.top_mask = pygame.mask.from_surface(self.top_pipe_image)
        self.bottom_mask = pygame.mask.from_surface(self.bottom_pipe_image)

    def move(self):
        """Move os canos para a esquerda.

        Atualiza a posição do cano na tela, movendo-o para a esquerda
        a uma velocidade constante.
        """
        self.x -= self.SPEED
        self._update_rect_positions()

    def _update_rect_positions(self):
        """Atualiza as posições dos retângulos de colisão dos canos.

        Ajusta as posições dos retângulos de colisão para refletir
        a nova posição do cano após o movimento.
        """
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen: pygame.Surface):
        """Desenha os canos na tela.

        Renderiza os canos superior e inferior na superfície fornecida.

        Args:
            screen (pygame.Surface): A superfície na qual os canos serão desenhados.
        """
        screen.blit(self.top_pipe_image, self.top_rect)
        screen.blit(self.bottom_pipe_image, self.bottom_rect)

    def check_collision(self, bird) -> bool:
        """Verifica se houve colisão com o pássaro.

        Verifica se a máscara do pássaro colide com as máscaras dos canos.

        Args:
            bird: A instância do pássaro a ser verificada a colisão.

        Returns:
            bool: 'True' se houve colisão, 'False' caso contrário.
        """
        bird_mask = bird.get_mask()

        top_offset = (self.top_rect.x - bird.rect.x, self.top_rect.y - bird.rect.y)
        bottom_offset = (self.bottom_rect.x - bird.rect.x, self.bottom_rect.y - bird.rect.y)

        return (
                bird_mask.overlap(self.top_mask, top_offset) is not None
                or bird_mask.overlap(self.bottom_mask, bottom_offset) is not None
        )
