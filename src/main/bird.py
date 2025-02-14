import pygame
from config import BIRD_IMAGES

class Bird:
    """Representa o pássaro no jogo Flappy Bird."""

    MAX_UP_ROTATION = 20
    MAX_DOWN_ROTATION = -90
    ROTATION_MULTIPLIER = -3
    ANIMATION_TIME = 5
    JUMP_FORCE = -8.3
    GRAVITY = 0.6
    MAX_FALL_SPEED = 10

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.vertical_speed = 0
        self.angle = 0
        self.animation_counter = 0
        self.current_image = BIRD_IMAGES[0]
        self.rotated_image = self.current_image
        self.rect = self.current_image.get_rect(center=(self.x, self.y))

    def jump(self):
        """Faz o pássaro pular."""
        if self.vertical_speed >= 0:  # Evita pular enquanto está subindo
            self.vertical_speed = self.JUMP_FORCE

    def move(self):
        """Atualiza a posição e rotação do pássaro."""
        self.vertical_speed = min(self.vertical_speed + self.GRAVITY, self.MAX_FALL_SPEED)
        self.y += self.vertical_speed

        # Atualiza o ângulo baseado na velocidade vertical
        self.angle = max(min(self.vertical_speed * self.ROTATION_MULTIPLIER, self.MAX_UP_ROTATION), self.MAX_DOWN_ROTATION)

    def update_animation(self):
        """Atualiza a animação de forma eficiente."""
        if self.angle <= -60:
            self.current_image = BIRD_IMAGES[1]  # Mantém as asas fixas
        else:
            self.animation_counter = (self.animation_counter + 1) % (self.ANIMATION_TIME * len(BIRD_IMAGES))
            frame_index = self.animation_counter // self.ANIMATION_TIME
            self.current_image = BIRD_IMAGES[frame_index]

    def draw(self, screen: pygame.Surface):
        """Desenha o pássaro na tela."""
        self.update_animation()
        self.rotated_image = pygame.transform.rotate(self.current_image, self.angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(self.rotated_image, self.rect.topleft)

    def get_mask(self) -> pygame.mask.Mask:
        """Retorna a máscara para detecção de colisões."""
        return pygame.mask.from_surface(self.rotated_image)
