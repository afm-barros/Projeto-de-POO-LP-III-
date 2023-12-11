import pygame

class Boss:
    
    

    def __init__(self, x, y, images, attack_images, direction='right', animation_speed=10):
        self.x = x
        self.y = y
        self.images = images
        self.direction = direction
        self.animation_speed = animation_speed
        self.health = 100
        self.max_health = 100 # Adicione a barra de vida aqui
        self.speed = 2
        self.current_image = 0
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()  # Adicione esta linha
        self.animation_counter = 0
        self.attack_damage = 10  # Adicione o dano do ataque aqui
        self.attacking_rect = None
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 2000
        self.attack_images = attack_images
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.invulnerability_timer = 0
        self.invulnerability_duration = 2000
        self.experience = 50

        

    def attack(self, hero):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = pygame.time.get_ticks()
        ATTACK_WIDTH = 200
        ATTACK_HEIGHT = 60
        center_x = self.x + self.width // 2
        attack_x = center_x - ATTACK_WIDTH // 2
        if self.direction == 'right':
            self.attacking_rect = pygame.Rect(attack_x, self.y + 75, ATTACK_WIDTH, ATTACK_HEIGHT)
        else:
            self.attacking_rect = pygame.Rect(attack_x, self.y + 75, ATTACK_WIDTH, ATTACK_HEIGHT)

        # Verifique se a hitbox de ataque colide com o Hero
        if self.attacking_rect.colliderect(hero.rect):
            # Diminua a saúde do Hero
            hero.health -= self.attack_damage
            if hero.health < 0:
                hero.health = 0

    def draw(self, screen):
        # Desenhe a imagem do boss
        if self.attacking:
            image = self.attack_images[self.current_image]
        else:
            image = self.images[self.current_image]

        if self.direction == 'right':
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, (self.x, self.y))

        # Desenhe a barra de vida no canto superior direito
        health_bar_x = screen.get_width() - 420
        health_bar_y = 20
        pygame.draw.rect(screen, (255, 255, 255), (health_bar_x - 2, health_bar_y - 2, 404, 24))  # Contorno branco
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, 400, 20))
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, 4 * (self.health / self.max_health) * 100, 20))

        font = pygame.font.Font("C:/Users/Augusto/Documents/ThaleahFat.ttf", 24)  # Escolha a fonte e o tamanho
        text = font.render('HORROR ANTIGO', True, (255, 255, 255))  # Crie o objeto de superfície do texto
        screen.blit(text, (health_bar_x, health_bar_y + 30))  # Desenhe o texto na tela

    def take_damage(self, amount):
        # Verifica se o boss é invulnerável
        if pygame.time.get_ticks() - self.invulnerability_timer < self.invulnerability_duration:
            return

        self.health -= amount
        if self.health < 0:
            self.health = 0

        # Boss se torna invulnerável após sofrer dano
        self.invulnerability_timer = pygame.time.get_ticks()


    def update(self, hero):
        self.hitbox.x = self.x
        self.hitbox.y = self.y
        if self.attacking:
            if pygame.time.get_ticks() - self.attack_timer > self.attack_duration:
                self.attacking = False
                self.attacking_rect = None
        else:
            # Se o Boss está à direita do herói, move o Boss para a esquerda
            if self.x > hero.rect.x:
                self.x -= self.speed
                self.direction = 'left'
            # Se o Boss está à esquerda do herói, move o Boss para a direita
            elif self.x < hero.rect.x:
                self.x += self.speed
                self.direction = 'right'

            # Se o Boss está perto o suficiente do herói, ataque
            if abs(self.x - hero.rect.x) < 50:
                self.attack(hero)

        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            # Se o contador de animação atingir a velocidade de animação, mude para a próxima imagem
            self.current_image = (self.current_image + 1) % len(self.images)
            self.animation_counter = 0