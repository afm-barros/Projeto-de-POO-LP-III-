import pygame


class Plataforma:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__rect = pygame.Rect(x, y, width, height)

    def __draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.__rect)

    def check_hero_on_top(self, hero):
        return hero.rect.colliderect(self.__rect)

    # Getter para rect
    def get_rect(self):
        return self.__rect

    # Setter para rect
    def set_rect(self, x, y, width, height):
        self.__rect = pygame.Rect(x, y, width, height)

    # Método para desenhar a plataforma
    def draw_platform(self, surface):
        self.__draw(surface)
