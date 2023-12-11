import pygame


class Hero():
    
    total_enemies_defeated = 0
    total_experience = 0

    def __init__(self, x, y, data, sprite_sheet, attack_sprite_sheet, move_sprites, animation_steps):

        self.size = data[0]
        self.image_scale = data[1]
        self.offset = [0, 10]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.attack_animation = self.load_images(attack_sprite_sheet, [1])
        self.move_animation = [pygame.transform.scale(pygame.image.load(
            sprite).convert_alpha(), (self.size, self.size)) for sprite in move_sprites]
        self.action = 0
        self.rect = pygame.Rect(
            (x, y - self.offset[1], self.size // self.image_scale, self.size // self.image_scale))
        self.vel_y = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.on_ground = False
        self.attack_type = 0
        self.facing = 'right'
        self.health = 100
        self.attack_cooldown = 0
        self.attack_counter = 0
        self.idle_delay_counter = 0
        self.flipped = False
        self.attack_animation_counter = 0
        self.move_animation_delay_counter = 0
        self.move_animation_delay = 30
        self.attacking_rect = pygame.Rect(0, 0, 0, 0)
        self.invulnerable = False
        self.vy = 0
        self.attack_damage = 7.5
        self.total_experience = 0

    def defeat_enemy(self):
        Hero.total_enemies_defeated += 1

    @staticmethod
    def get_total_enemies_defeated():
        return Hero.total_enemies_defeated

    def get_total_experience(self):  
        return self.total_experience
    
    def reset_experience(self):
        self.total_experience = 0
    
    def gain_experience(self, amount):
        self.total_experience += amount

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        sprite_width, sprite_height = 58, 54  # Tamanho de cada sprite

        sprite_width = min(sprite_width, sprite_sheet.get_width())
        sprite_height = min(sprite_height, sprite_sheet.get_height())

        sprites_per_row = sprite_sheet.get_width() // sprite_width
        if sprites_per_row == 0:
            sprites_per_row = 1
        sprites_per_column = sprite_sheet.get_height() // sprite_height

        for i, animation in enumerate(animation_steps):
            temp_img_list = []
            for j in range(animation):
                x = (j % sprites_per_row) * sprite_width
                y = (i % sprites_per_column) * sprite_height
                temp_img = sprite_sheet.subsurface(
                    pygame.Rect(x, y, sprite_width, sprite_height))
                # Redimensionar a imagem do sprite
                temp_img = pygame.transform.scale(
                    temp_img, (self.size, self.size))
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface,  target=None, plataformas=None):
        SPEED = 2.5
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if plataformas is not None:
            for plataforma in plataformas:
                # Se o personagem está caindo e a parte de baixo do personagem está colidindo com a plataforma
                # Verifica se o herói está acima da plataforma
                if self.vel_y > 0 and pygame.Rect.colliderect(self.rect, plataforma):
                    if self.rect.bottom - self.vel_y <= plataforma.top:
                        self.vel_y = 0  # Parar a queda
                        self.on_ground = True  # O personagem está no chão
                        # Posicionar o personagem em cima da plataforma # Posicionar o personagem em cima da plataforma
                        self.rect.y = plataforma.top - self.rect.height

        if self.action != 6:
            if key[pygame.K_a] or key[pygame.K_d]:
                self.move_animation_delay_counter += 1
                if self.move_animation_delay_counter >= self.move_animation_delay:
                    self.frame_index = (
                        self.frame_index + 1) % len(self.move_animation)
                    self.move_animation_delay_counter = 0

                if key[pygame.K_a]:
                    dx = -SPEED
                    self.facing = 'left'
                    self.flipped = True
                    if self.action != 1:
                        self.frame_index = 0
                    self.action = 1
                elif key[pygame.K_d]:
                    dx = SPEED
                    self.facing = 'right'
                    self.flipped = False
                    if self.action != 2:
                        self.frame_index = 0
                    self.action = 2
                else:
                    if self.action != 0:
                        self.frame_index = 0
                    self.action = 0

        if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
            dx = 0

        if self.rect.top + dy <= 0 or self.rect.bottom + dy > screen_height:
            dy = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.action != 6:
            self.frame_index = (self.frame_index +
                                1) % len(self.move_animation)

        if key[pygame.K_SPACE] and (self.on_ground):
            self.vel_y = -18
            self.on_ground = False
        if key[pygame.K_r] or key[pygame.K_t]:
            if self.action != 6:  # Adicionar esta linha
                if target is None:
                    if self.facing == 'right':
                        target = pygame.Rect(
                            self.rect.right, self.rect.y, self.rect.width, self.rect.height)
                    else:
                        target = pygame.Rect(
                            self.rect.left - self.rect.width, self.rect.y, self.rect.width, self.rect.height)
                self.attack(surface, target)

        if key[pygame.K_r]:
            self.attack_type = 1
        if key[pygame.K_t]:
            self.attack_type = 2

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        if self.rect.bottom + dy > screen_height - 75 and dy > 0:
            dy = screen_height - 30 - self.rect.bottom
            self.on_ground = True

        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, targets):
        self.action = 6
        if self.attack_cooldown == 0:
            attack_width = 1.3 * self.rect.width
            if self.facing == 'right':
                self.attacking_rect = pygame.Rect(
                    self.rect.centerx, self.rect.y, attack_width, self.rect.height)
            else:
                self.attacking_rect = pygame.Rect(
                    self.rect.centerx - attack_width, self.rect.y, attack_width, self.rect.height)

            # Itera sobre a lista de alvos
            for target in targets:
                # Verifica se o ataque colide com o alvo
                if self.attacking_rect.colliderect(target.rect):
                    self.total_experience += target.experience  # Aqui é onde a experiência do herói é aumentada
                    self.attack_cooldown = 5
                    break  # Para de verificar após o primeiro alvo atingido

    def update(self):
        # Decrementa o cooldown do ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.action == 6:  # Se o herói está atacando
            self.attack_animation_counter += 1
            if self.attack_animation_counter >= 30:  # Se o contador de atraso atingiu o limite
                self.frame_index = (self.frame_index +
                                    1) % len(self.attack_animation[0])
            # Se a animação de ataque terminou
            if self.frame_index == len(self.attack_animation[0]) - 1:
                self.action = 0  # Alterar a ação de volta para a ação de movimento
                self.frame_index = 0  # Resetar o índice do quadro
                self.attack_animation_counter = 0  # Resetar o contador de atraso
                self.attacking_rect = None  # Resetar o retângulo de ataque
        # Se o herói estiver se movendo para a direita ou esquerda
        elif self.action in [1, 2]:
            self.flipped = self.action == 1
            self.move_animation_delay_counter += 1
            if self.move_animation_delay_counter >= self.move_animation_delay:
                self.frame_index = (self.frame_index +
                                    1) % len(self.move_animation)
                self.move_animation_delay_counter = 0
            # Atualizar o índice do frame
            self.frame_index = (self.frame_index +
                                1) % len(self.move_animation)
        else:
            self.frame_index = (self.frame_index +
                                1) % len(self.animation_list[self.action])

    def draw(self, surface):
        RED = (255, 0, 0)  # Definir a cor vermelha
     #   pygame.draw.rect(surface, RED, self.rect, 2)
        if self.action == 6:  # Se o herói estiver atacando
            image = self.attack_animation[0][self.frame_index % len(
                self.attack_animation[0])]  # Usar a animação de ataque
        elif self.action in [1, 2]:  # Se o herói estiver se movendo
            image = self.move_animation[self.frame_index %
                                        len(self.move_animation)]
        else:
            if self.idle_delay_counter < 20:  # Se o atraso da animação idle ainda não tiver terminado
                image = self.animation_list[self.action][self.frame_index % len(
                    self.animation_list[self.action])]
            else:
                image = None
        if image is not None:
            image = pygame.transform.flip(image, not self.flipped, False)
            x = self.rect.x + (self.rect.width - image.get_width()) // 2
            y = self.rect.y + (self.rect.height - image.get_height()) // 2
            surface.blit(image, (x, y))
