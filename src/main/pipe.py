import random

import pygame

from config import PIPE_IMAGE, SCREEN_HEIGHT
from constants import PIPE_SPEED
from floor import Floor


class Pipe(pygame.sprite.Sprite):
    """Representa os canos do jogo Flappy Bird."""

    SPEED = PIPE_SPEED
    GAP = 150

    def __init__(self, x: int):
        super().__init__()
        self.x = x
        self.pipe_image = None
        self.top_pipe_image = None
        self.bottom_pipe_image = None
        self.ground_height = None
        self.ground_level = None
        self.pipe_height = None
        self.MIN_HEIGHT = None
        self.MAX_HEIGHT = None
        self.height = None
        self.top_y = None
        self.bottom_y = None
        self.top_rect = None
        self.bottom_rect = None
        self.passed = False
        self.top_mask = None
        self.bottom_mask = None

        self.setup_pipe_images()
        self.setup_dimensions()
        self.generate_heights()
        self.setup_rects()
        self.calculate_masks()

    def setup_pipe_images(self):
        """Configura as imagens do cano."""
        self.pipe_image = PIPE_IMAGE
        self.top_pipe_image = pygame.transform.flip(self.pipe_image, False, True)
        self.bottom_pipe_image = self.pipe_image

    def setup_dimensions(self):
        """Configura as dimensões dos canos."""
        self.ground_height = Floor.IMAGE.get_height()
        self.ground_level = SCREEN_HEIGHT - self.ground_height
        self.pipe_height = self.pipe_image.get_height()
        self.MIN_HEIGHT = self.pipe_height // 4
        self.MAX_HEIGHT = self.ground_level - self.GAP - self.pipe_height // 4
        if self.MAX_HEIGHT <= self.MIN_HEIGHT:
            self.MAX_HEIGHT = self.MIN_HEIGHT + 50

    def generate_heights(self):
        """Gera as alturas dos canos."""
        self.height = random.randint(self.MIN_HEIGHT, self.MAX_HEIGHT)
        self.top_y = self.height - self.pipe_height
        self.bottom_y = self.height + self.GAP

    def setup_rects(self):
        """Configura os retângulos dos canos."""
        self.top_rect = self.top_pipe_image.get_rect(x=self.x, y=self.top_y)
        self.bottom_rect = self.bottom_pipe_image.get_rect(x=self.x, y=self.bottom_y)

    def calculate_masks(self):
        """Calcula as máscaras de colisão."""
        self.top_mask = pygame.mask.from_surface(self.top_pipe_image)
        self.bottom_mask = pygame.mask.from_surface(self.bottom_pipe_image)

    def move(self):
        """Move os canos para a esquerda."""
        self.x -= self.SPEED
        self.update_rect_positions()

    def update_rect_positions(self):
        """Atualiza as posições dos retângulos dos canos."""
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen: pygame.Surface):
        """Desenha os canos na tela."""
        screen.blit(self.top_pipe_image, self.top_rect)
        screen.blit(self.bottom_pipe_image, self.bottom_rect)

    def check_collision(self, bird) -> bool:
        """Verifica colisão com o pássaro."""
        bird_mask = bird.get_mask()
        top_offset = (self.top_rect.x - bird.rect.x, self.top_rect.y - bird.rect.y)
        bottom_offset = (self.bottom_rect.x - bird.rect.x, self.bottom_rect.y - bird.rect.y)
        return bird_mask.overlap(self.top_mask, top_offset) or bird_mask.overlap(self.bottom_mask, bottom_offset)
