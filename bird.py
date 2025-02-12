import pygame
from config import BIRD_FRAMES


class Bird:
    MAX_ROTATION_ANGLE = 25
    ROTATION_SPEED = 20
    FRAME_CHANGE_INTERVAL = 5
    JUMP_FORCE = -10.5
    GRAVITY_FORCE = 1.5
    MAX_FALL_SPEED = 16

    def __init__(self, start_x: int, start_y: int):
        self.x_position = start_x
        self.y_position = start_y
        self.rotation_angle = 0
        self.vertical_speed = 0
        self.initial_height = start_y
        self.time_in_air = 0
        self.animation_frame_index = 0
        self.current_image = BIRD_FRAMES[0]

    def jump(self):
        """Faz o pássaro pular, ajustando a velocidade e reiniciando o tempo de queda."""
        self.vertical_speed = self.JUMP_FORCE
        self.time_in_air = 0
        self.initial_height = self.y_position

    def move(self):
        """Calcula o deslocamento do pássaro baseado na gravidade e sua velocidade."""
        self.time_in_air += 1
        displacement = self.GRAVITY_FORCE * (self.time_in_air ** 2) + self.vertical_speed * self.time_in_air

        # Limita a velocidade de queda
        displacement = min(displacement, self.MAX_FALL_SPEED)

        # Acelera um pouco a subida
        if displacement < 0:
            displacement -= 2

        self.y_position += displacement

        # Ajusta a rotação do pássaro
        if displacement < 0 or self.y_position < (self.initial_height + 50):
            self.rotation_angle = min(self.rotation_angle + self.ROTATION_SPEED, self.MAX_ROTATION_ANGLE)
        else:
            self.rotation_angle = max(self.rotation_angle - self.ROTATION_SPEED, -90)

    def draw(self, screen: pygame.Surface):
        """Desenha o pássaro na tela com a animação correta."""
        self.animation_frame_index = (self.animation_frame_index + 1) % (self.FRAME_CHANGE_INTERVAL * 4)

        # Define qual imagem usar para animação
        animation_sequence = [0, 1, 2, 1]  # Ordem de animação das asas
        self.current_image = BIRD_FRAMES[animation_sequence[self.animation_frame_index // self.FRAME_CHANGE_INTERVAL]]

        # Se o pássaro estiver caindo, fixa a asa no meio
        if self.rotation_angle <= -80:
            self.current_image = BIRD_FRAMES[1]
            self.animation_frame_index = self.FRAME_CHANGE_INTERVAL * 2

        # Rotaciona a imagem mantendo a posição correta
        rotated_image = pygame.transform.rotate(self.current_image, self.rotation_angle)
        rotated_image_rect = rotated_image.get_rect(center=(self.x_position, self.y_position))
        screen.blit(rotated_image, rotated_image_rect.topleft)

    def get_mask(self) -> pygame.mask.Mask:
        """Retorna a máscara do pássaro para detecção de colisão."""
        return pygame.mask.from_surface(self.current_image)
