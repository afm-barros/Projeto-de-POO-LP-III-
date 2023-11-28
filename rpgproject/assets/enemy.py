import pygame

SCREEN_WIDTH = 800


class Enemy:
    def __init__(self, x, y, images, direction):
        self.x = x
        self.y = y
        self.images = images
        self.current_image = 0
        self.direction = direction
        self.animation_counter = 0
        self.animation_speed = 10
        self.rect = self.images[self.current_image].get_rect(
            topleft=(self.x, self.y))

    def move(self):
        if self.direction == 'right':
            self.x += 1
            if self.x >= SCREEN_WIDTH:
                self.direction = 'left'
                self.images = [pygame.transform.flip(
                    image, True, False) for image in self.images]
                self.x = SCREEN_WIDTH
        else:
            self.x -= 1
            if self.x <= 0:
                self.direction = 'right'
                self.images = [pygame.transform.flip(
                    image, True, False) for image in self.images]
                self.x = 0
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.images[self.current_image], (self.x, self.y))
      #  pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Desenha a hitbox

    def update(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.animation_counter = 0

        return True
