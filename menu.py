import pygame
from pygame.locals import *


class Menu:
    def __init__(self, screen_width=800, screen_height=600, font_path="C:/Users/Augusto/Documents/ThaleahFat.ttf", title="Dungeon Project"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.font = pygame.font.Font(font_path, 50)
        self.title_font = pygame.font.Font(font_path, 70)
        self.title = title
        self.options = ["Iniciar Jogo", "Creditos", "Sair"]
        self.index = 0
        self.background = pygame.image.load(
            "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/background/menubackground.jpg")

    @classmethod
    def from_config(cls, config):
        return cls(config['screen_width'], config['screen_height'], config['font_path'], config['title'])

    def draw_text(self, text, y, selected=False):
        font = self.title_font if selected else self.font
        surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (self.screen_width /
                         2 - surface.get_width()/2, y))

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text(self.title, self.screen_height/4,
                       selected=True)
        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                center=(self.screen_width/2, self.screen_height/2 + i*60))
            if i == self.index:
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 text_rect.inflate(20, 20), 2)
            self.screen.blit(text_surface, text_rect)

    def display_victory_screen(self, total_experience, total_enemies_defeated):
        options = ["Voltar"]
        index = 0
        victory_background = pygame.image.load(
            "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/background/victory.jpg")
        self.screen.blit(victory_background, (0, 0))
        font = self.title_font
        surface = font.render("Voce venceu!", True, (91, 217, 171))
        self.screen.blit(surface, (self.screen_width / 2 - surface.get_width()/2, self.screen_height/9))
        # Adicionando a experiência total adquirida
        experience_surface = self.font.render(f"Total XP: {total_experience}", True, (230, 192, 32))
        self.screen.blit(experience_surface, (self.screen_width - experience_surface.get_width(), self.screen_height - experience_surface.get_height()))
        # Adicionando o total de inimigos derrotados
        enemies_surface = self.font.render(f"Inimigos derrotados: {total_enemies_defeated}", True, (230, 192, 32))
        self.screen.blit(enemies_surface, (self.screen_width - enemies_surface.get_width(), self.screen_height - enemies_surface.get_height() - 30))

        # Restante do código...
        while True:
            for i, option in enumerate(options):
                text_surface = self.font.render(option, True, (255, 255, 255))
                text_rect = text_surface.get_rect(
                    center=(self.screen_width/2, self.screen_height/2 + i*60))
                if i == index:
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     text_rect.inflate(20, 20), 2)
                self.screen.blit(text_surface, text_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return

    def display_death_screen(self):
        options = ["Continuar"]
        index = 0
        defeat_background = pygame.image.load(
            "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/background/defeat.jpg")
        self.screen.blit(defeat_background, (0, 0))
        self.draw_text("Voce morreu!", self.screen_height/4, selected=True)
        while True:
            for i, option in enumerate(options):
                text_surface = self.font.render(option, True, (255, 255, 255))
                text_rect = text_surface.get_rect(
                    center=(self.screen_width/2, self.screen_height/2 + i*60))
                if i == index:
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     text_rect.inflate(20, 20), 2)
                self.screen.blit(text_surface, text_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return

    def display_credits(self):
        credits = ["Desenvolvedor: Augusto Fagundes M. Barros", "Professor: Dany Sanchez Dominguez",
                   "Disciplina: LP III", "Universidade Estadual de Santa Cruz", "", "Pressione qualquer tecla para voltar"]
        self.screen.fill((0, 0, 0))
        for i, line in enumerate(credits):
            self.draw_text(line, self.screen_height/4 + i*60)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    return

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.index = (self.index - 1) % len(self.options)
                    elif event.key == K_DOWN:
                        self.index = (self.index + 1) % len(self.options)
                    elif event.key == K_RETURN:
                        if self.index == 0:
                            return 'start'
                        elif self.index == 1:
                            self.display_credits()
                        elif self.index == 2:
                            return 'quit'
            self.draw_menu()
            pygame.display.update()
        pygame.quit()
