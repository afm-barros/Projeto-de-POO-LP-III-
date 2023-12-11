import pygame
from pygame import USEREVENT
from hero import Hero
from menu import Menu
from enemy import Enemy
from plataformas import Plataforma
from boss import Boss


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
def draw_text(screen, text, size, x, y):
    font = pygame.font.Font('C:/Users/Augusto/Documents/ThaleahFat.ttf', size)  # Substitua pelo caminho para sua fonte
    text_surface = font.render(text, True, (255, 253, 138))
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (x, y)  # Altere para posicionar no canto inferior direito
    screen.blit(text_surface, text_rect)

def game_loop(screen, clock, FPS, bg_image, RED, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, menu):
    Hero_1 = initialize_hero(SCREEN_WIDTH)
    total_enemies_defeated = 0
    door = Door(0, Hero_1.rect.y, 140, 300)
    ghosts = []
    plataformas = []
    boss = None

    level = 1
    
    run = True
    while run:
        clock.tick(FPS)

        
        draw_bg(screen, bg_image, SCREEN_WIDTH, SCREEN_HEIGHT)

    
        draw_health_bar(screen, Hero_1.health, 20, 20, RED, WHITE)
        draw_text(screen, f"Xp: {Hero_1.get_total_experience()}", 30, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10)

        if level == 3:
            #for plataforma in plataformas:
                #plataforma.draw(screen)
            Hero_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, ghosts, [plataforma.get_rect() for plataforma in plataformas])
        else:
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
                    Hero_1.gain_experience(ghost.experience)
                    total_enemies_defeated += 1
            if Hero_1.rect.colliderect(ghost.rect) and not Hero_1.invulnerable:
                Hero_1.health -= 10
                Hero_1.invulnerable = True
                pygame.time.set_timer(USEREVENT + 1, 1000)
                PUSH_BACK_AMOUNT = 50
                if Hero_1.rect.x < ghost.rect.x:
                    Hero_1.rect.x -= PUSH_BACK_AMOUNT
                else:
                    Hero_1.rect.x += PUSH_BACK_AMOUNT

                if Hero_1.rect.y < ghost.rect.y:
                    Hero_1.rect.y -= PUSH_BACK_AMOUNT
                else:
                    Hero_1.rect.y += PUSH_BACK_AMOUNT

                Hero_1.rect.x += 50
                Hero_1.vy = -10
        if Hero_1.health <= 0:
            Hero_1.reset_experience()
            menu.display_death_screen()
            run = False

        if door.hero_hit(Hero_1):
            # Adicione esta lógica antes de mudar de nível
            for ghost in ghosts:
                Hero_1.gain_experience(ghost.experience)
            ghosts = []

            if level == 1:
                level += 1
                bg_image = pygame.image.load(
                    "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/background/room1.jpg").convert_alpha()
                Hero_1.rect.x = SCREEN_WIDTH - Hero_1.rect.width
                Hero_1.rect.y = 310
                ghost_images = [
                    pygame.image.load(
                        'C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/ghost.png'),
                    pygame.image.load(
                        'C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/ghost2.png')
                ]
                for i in range(4):  # Adicionando um inimigo extra no nível 2
                    ghost = Enemy(50 + i * 200, 485, ghost_images, 'right', 100)
                    ghosts.append(ghost)
            # Restante do código...
            elif level == 2:
                level += 1
                bg_image = pygame.image.load(
                    "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/background/room2.jpg").convert_alpha()
                Hero_1.rect.x = SCREEN_WIDTH - Hero_1.rect.width
                Hero_1.rect.y = 310
                ghost_images = [
                    pygame.image.load(
                        'C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/ghost.png'),
                    pygame.image.load(
                        'C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/ghost2.png')
                ]
                
                for i in range(6):  # Adicionando mais inimigos no nível 3
                    ghost = Enemy(50 + i * 150, 140, ghost_images, 'right', 100)
                    ghosts.append(ghost)
                plataformas = [Plataforma(390, 360, 130, 250), Plataforma(600, 510, 130, 120)]
                for plataforma in plataformas:
                    plataforma.set_rect(plataforma.x, plataforma.y, plataforma.width, plataforma.height)

            
            elif level == 3:
                level += 1
                bg_image = pygame.image.load(
                    "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/background/room3.jpg").convert_alpha()
                Hero_1.rect.x = SCREEN_WIDTH - Hero_1.rect.width
                Hero_1.rect.y = 310
                # Limpe a lista de fantasmas e plataformas para o nível 4
                ghosts = []
                plataformas = []
                # Adicione o chefe final
                boss_images = [
                    pygame.image.load('C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/boss.png'),
                ]


                boss_image1 = pygame.image.load('C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/bosswalk.png')
                boss_image2 = pygame.image.load('C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/bosswalk2.png')
                
                boss_attack_images = [
                    pygame.image.load('C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/bossattack1.png'),
                    pygame.image.load('C:/Users/Augusto/NovaPasta/rpgproject/assets/images/enemy/bossattack2.png')
                ]

                boss = Boss(50, 426, [boss_image1, boss_image2], boss_attack_images, 'right')      
        if level == 4 and boss is not None:
            boss.draw(screen)
            boss.update(Hero_1)
            if Hero_1.attacking_rect is not None:
                if Hero_1.attacking_rect.colliderect(boss.hitbox):
                    boss.take_damage(Hero_1.attack_damage)
                    if boss.health <= 0:
                        Hero_1.gain_experience(boss.experience)
                        total_enemies_defeated += 1  
                        boss = None
            if Hero_1.health <= 0:
                menu.display_death_screen(Hero_1.get_total_experience(), total_enemies_defeated)
                run = False
        if level == 4 and boss is None:
            menu.display_victory_screen(Hero_1.get_total_experience(), total_enemies_defeated)
            run = False

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
            game_loop(screen, clock, FPS, bg_image, RED, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, menu)

        elif menu_option == 'quit':
            run = False

    pygame.quit()


if __name__ == "__main__":
    main()
