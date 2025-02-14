import random

import pygame

from config import PIPE_IMAGE, SCREEN_HEIGHT
from constants import PIPE_SPEED
from floor import Floor


class Pipe:
    """Representa os canos do jogo Flappy Bird."""

    SPEED = PIPE_SPEED
    GAP = 150

    def __init__(self, x: int):
        self.x = x
        self.pipe_image = PIPE_IMAGE
        self.ground_height = Floor.IMAGE.get_height()
        self.ground_level = SCREEN_HEIGHT - self.ground_height
        self.pipe_height = self.pipe_image.get_height()

        self.MIN_HEIGHT = self.pipe_height // 4
        self.MAX_HEIGHT = self.ground_level - self.GAP - self.pipe_height // 4

        if self.MAX_HEIGHT <= self.MIN_HEIGHT:
            self.MAX_HEIGHT = self.MIN_HEIGHT + 50

        self.height = random.randint(self.MIN_HEIGHT, self.MAX_HEIGHT)
        self.top_y = self.height - self.pipe_height
        self.bottom_y = self.height + self.GAP

        self.top_pipe_image = pygame.transform.flip(self.pipe_image, False, True)
        self.bottom_pipe_image = self.pipe_image

        self.top_rect = self.top_pipe_image.get_rect(x=self.x, y=self.top_y)
        self.bottom_rect = self.bottom_pipe_image.get_rect(x=self.x, y=self.bottom_y)
        self.passed = False

    def move(self):
        """Move os canos para a esquerda."""
        self.x -= self.SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen: pygame.Surface):
        """Desenha os canos na tela."""
        screen.blit(self.top_pipe_image, self.top_rect)
        screen.blit(self.bottom_pipe_image, self.bottom_rect)

    def check_collision(self, bird) -> bool:
        """Verifica colisão com o pássaro."""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_pipe_image)
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe_image)

        # Deslocamento de máscara otimizado
        top_offset = (self.top_rect.x - bird.rect.x, self.top_rect.y - bird.rect.y)
        bottom_offset = (self.bottom_rect.x - bird.rect.x, self.bottom_rect.y - bird.rect.y)

        # Verificação de colisão eficiente
        return bird_mask.overlap(top_mask, top_offset) or bird_mask.overlap(bottom_mask, bottom_offset)
