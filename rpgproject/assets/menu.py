import pygame
from pygame.locals import *


class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(
            None, 70)  # Fonte maior para o título
        self.title = "Dungeon Project"
        self.options = ["Iniciar Jogo", "Créditos", "Sair"]
        self.index = 0
        self.background = pygame.image.load(
            "C:/Users/Augusto/NovaPasta/rpgproject/assets/images/background/menubackground.jpg")  # Carrega a imagem de fundo

    def draw_text(self, text, y, selected=False):
        font = self.title_font if selected else self.font
        surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (self.screen_width /
                         2 - surface.get_width()/2, y))

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))  # Desenha a imagem de fundo
        self.draw_text(self.title, self.screen_height/4,
                       selected=True)  # Desenha o título
        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                center=(self.screen_width/2, self.screen_height/2 + i*60))
            if i == self.index:
                # Desenha um retângulo em torno da opção selecionada
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 text_rect.inflate(20, 20), 2)
            self.screen.blit(text_surface, text_rect)

    def display_credits(self):
        credits = ["Desenvolvedor: Augusto Fagundes Moreira Barros", "Professor: Dany Sanchez Dominguez",
                   "Disciplina: LP III", "Universidade Estadual de Santa Cruz", "", "Pressione qualquer tecla para voltar"]
        self.screen.fill((0, 0, 0))
        for i, line in enumerate(credits):
            self.draw_text(line, self.screen_height/4 + i*60)
        pygame.display.update()

        while True:  # Loop até que uma tecla seja pressionada
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN:
                    return  # Retorna ao menu quando uma tecla é pressionada

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
