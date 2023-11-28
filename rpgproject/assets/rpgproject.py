import pygame
from pygame import USEREVENT
from hero import Hero
from menu import Menu
from enemy import Enemy


class Door:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def hero_hit(self, hero):
        return self.rect.colliderect(hero.rect)


def initialize_hero(SCREEN_WIDTH):
    HERO_SIZE = 192
    HERO_SCALE = 4
    HERO_OFFSET = [72, 70]
    HERO_DATA = [HERO_SIZE, HERO_SCALE, HERO_OFFSET]
    HERO_ANIMATION_STEPS = [2, 8, 4, 2, 4, 10, 6]

    hero_1_sheet = pygame.image.load(
        "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/hero/sprites/hero.png").convert_alpha()

    hero_1_attack_sheet = pygame.image.load(
        "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/hero/sprites/heroatacando.png").convert_alpha()

    hero_1_move_sprite_1 = "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/hero/sprites/heromovendo1.png"
    hero_1_move_sprite_2 = "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/hero/sprites/heromovendo2.png"
    hero_1_move_sprites = [hero_1_move_sprite_1, hero_1_move_sprite_2]

    hero = Hero(SCREEN_WIDTH - HERO_SIZE, 310, HERO_DATA, hero_1_sheet,
                hero_1_attack_sheet, hero_1_move_sprites, HERO_ANIMATION_STEPS)

    return hero


def draw_bg(screen, bg_image, SCREEN_WIDTH, SCREEN_HEIGHT):
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


def draw_health_bar(screen, health, x, y, RED, WHITE):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 24))
    pygame.draw.rect(screen, RED, (x, y, 400 * ratio, 20))


def game_loop(screen, clock, FPS, bg_image, RED, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT):
    Hero_1 = initialize_hero(SCREEN_WIDTH)
    door = Door(0, Hero_1.rect.y, 140, 300)
    ghosts = []

    run = True
    while run:
        clock.tick(FPS)

        draw_bg(screen, bg_image, SCREEN_WIDTH, SCREEN_HEIGHT)

        draw_health_bar(screen, Hero_1.health, 20, 20, RED, WHITE)

        Hero_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, ghosts)
        Hero_1.update()

        Hero_1.draw(screen)

        for ghost in ghosts[:]:
            ghost.move()
            ghost.update()
            ghost.draw(screen)
            if Hero_1.attacking_rect is not None:
                if Hero_1.attacking_rect.colliderect(ghost.rect):
                    ghosts.remove(ghost)
            if Hero_1.rect.colliderect(ghost.rect) and not Hero_1.invulnerable:
                Hero_1.health -= 33
                Hero_1.invulnerable = True
                pygame.time.set_timer(USEREVENT + 1, 2000)
                Hero_1.rect.x += 50
        if Hero_1.health <= 0:
            run = False

        if door.hero_hit(Hero_1):
            bg_image = pygame.image.load(
                "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/background/room1.jpg").convert_alpha()
            Hero_1.rect.x = Hero_1.rect.x = SCREEN_WIDTH - Hero_1.rect.width
            Hero_1.rect.y = 310
            ghost_images = [
                pygame.image.load(
                    'C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/ghost.png'),
                pygame.image.load(
                    'C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/ghost2.png')
            ]
            for i in range(3):
                ghost = Enemy(50 + i * 200, 485, ghost_images, 'right')
                ghosts.append(ghost)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == USEREVENT + 1:
                Hero_1.invulnerable = False

        pygame.display.update()


def main():
    pygame.init()

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG")

    clock = pygame.time.Clock()
    FPS = 60

    RED = (201, 34, 34)
    WHITE = (255, 255, 255)

    bg_image = pygame.image.load(
        "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/background/background.jpg").convert_alpha()

    menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)

    run = True
    while run:
        menu_option = menu.run()

        if menu_option == 'start':
            game_loop(screen, clock, FPS, bg_image, RED,
                      WHITE, SCREEN_WIDTH, SCREEN_HEIGHT)

        elif menu_option == 'quit':
            run = False

    pygame.quit()


if __name__ == "__main__":
    main()
