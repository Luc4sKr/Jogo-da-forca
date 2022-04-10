import pygame # Para instalar -> pip3 install pygame
from random import randint
from sys import exit

pygame.init()

class Forca:
    def __init__(self):
        # -- Tela do jogo -----------------------------------------------------
        self.SCREEN_X, self.SCREEN_Y = 480, 520
        self.screen = pygame.display.set_mode((self.SCREEN_X, self.SCREEN_Y))
        pygame.display.set_caption("Jogo da forca")

        # -- Cria um objeto para ajudar a controlar o tempo -------------------
        self.clock = pygame.time.Clock()

        # -- Variáveis para input de usuário ----------------------------------
        self.base_font = pygame.font.Font(None, 32)
        self.user_text = ""
        self.input_rect = pygame.Rect(self.SCREEN_X/2 - 140/2, 350, 140, 32)
        self.color = pygame.Color("white")

        self.new_game()


    def new_game(self):
        self.letras_corretas = []
        self.letras_jogadas = []

        self.arquivo = open("palavras.txt", "r")
        self.random_num = randint(0, len(self.arquivo.readlines()) - 1)

        self.arquivo = open("palavras.txt", "r")
        self.palavra_sorteada = self.arquivo.readlines()[self.random_num]
        self.palavra_sorteada = self.palavra_sorteada[0:len(self.palavra_sorteada) - 1]

        print(self.palavra_sorteada)

        for letras_da_palavra in self.palavra_sorteada:
             self.letras_corretas.append("_ ")

        self.erros = 5

        self.game_over = False
        self.tela_vitoria = False
        self.tela_derrota = False
        self.jogo()


    def jogo(self):
        while not self.game_over:
            self.screen.fill((0, 0, 0))

            self.forca()

            self.draw(str(self.letras_corretas).strip("[]").replace("'", ""), 32, (255, 255, 255), self.SCREEN_X/2, 300)
            self.draw(f"Letras jogadas: {str(self.letras_jogadas)}".replace("'", ""), 20, (255, 255, 255), 10, 400, True, False)

            pygame.draw.rect(self.screen, self.color, self.input_rect, 2)
            self.text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
            self.screen.blit(self.text_surface, (self.SCREEN_X/2, self.input_rect.y + 5))

            if self.letras_corretas.count("_ ") == 0: # Precisa ser "_ " pois la lista tem um espaço separa separar melhor as palavras
                self.tela_vitoria = True
                self.game_over = True
                self.tela_de_vitoria()

            if self.erros == 0:
                self.tela_derrota = True
                self.game_over = True
                self.tela_de_derrota()

            self.events()

            pygame.display.update()
            pygame.display.flip()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # -- Verifica se o usuário não digitou nada ---------------
                    if self.user_text == "":
                        break

                    # -- Verifica e adiciona a letra que o usuário digitou ----
                    c = 0
                    for i in self.palavra_sorteada.upper():
                        if self.user_text.upper() == i.upper():
                            self.letras_corretas.insert(c, i)
                            self.letras_corretas.pop(c+1)
                        c += 1

                    # -- Adiciona as letras jogadas em uma lista --------------
                    self.letras_jogadas.append(self.user_text)
                    self.letras_jogadas.sort()
                    if self.letras_jogadas.count(self.user_text) > 1:
                        self.letras_jogadas.remove(self.user_text)
                        self.letras_jogadas.sort()
                    print(self.letras_jogadas)

                    # -- Verifica se a letra não exite na palavra -------------
                    if self.user_text.upper() not in self.letras_corretas:
                        self.erros -= 1

                    self.user_text = ""

                # Recebe os inputs das letras ---------------------------------
                else:
                    self.user_text = event.unicode


    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.new_game()


    def tela_de_vitoria(self):
        while self.tela_vitoria:
            self.draw("VOCÊ GANHOU", 50, (0, 255, 0), self.SCREEN_X / 2, 30, False, True)
            self.draw("PRESSIONE 'SPACE' PARA JOGAR NOVAMENTE", 15, (0, 255, 0), self.SCREEN_X / 2, 480, False, True)

            self.game_over_events()

            pygame.display.flip()


    def tela_de_derrota(self):
        while self.tela_derrota:
            self.draw("VOCÊ PERDEU", 50, (255, 0, 0), self.SCREEN_X / 2, 30, False, True)
            self.draw("PRESSIONE 'SPACE' PARA JOGAR NOVAMENTE", 15, (255, 0, 0), self.SCREEN_X / 2, 480, False, True)

            self.game_over_events()

            pygame.display.flip()


    def draw(self, text, tam, color, x, y, draw_left=False, arialblack=False):
        self.fonte = pygame.font.Font(pygame.font.match_font("arial"), tam)
        if arialblack:
            self.fonte = pygame.font.Font(pygame.font.match_font("arialblack"), tam)

        self.obj = self.fonte.render(text, False, color)
        self.obj_rect = self.obj.get_rect()
        self.obj_rect.center = (x, y)
        if draw_left:
            self.obj_rect.left = x
            self.obj_rect.y = y

        self.screen.blit(self.obj, self.obj_rect)


    def forca(self):
        # -- Forca -----------------------------------------------------
        self.draw("|", 100, (255, 255, 255), 100, 100)
        self.draw("|", 100, (255, 255, 255), 100, 190)
        self.draw("_", 100, (255, 255, 255), 121, 15)
        self.draw("_", 100, (255, 255, 255), 168, 15)
        self.draw("|", 50, (255, 255, 255), 190, 80)

        # -- Partes do corpo --------------------------------------------
        self.draw("O", 50, (255, 255, 255), 190, 125) # Cabeça
        if self.erros >= 1:
            self.draw("|", 50, (255, 255, 255), 190, 160) # Tronco
        if self.erros >=2:
            self.draw("/", 50, (255, 255, 255), 185, 170) # Braço esquerdo
        if self.erros >= 3:
            self.draw("\\", 50, (255, 255, 255), 195, 170) # Braço direito
        if self.erros >= 4:
            self.draw("/", 50, (255, 255, 255), 185, 200) # Perna direita
        if self.erros == 5:
            self.draw("\\", 50, (255, 255, 255), 195, 200) # Perna esquerda

        if self.erros == 0:
            self.draw("X", 10, (255, 255, 255), 186, 120)
            self.draw("X", 10, (255, 255, 255), 196, 120)



if __name__ == '__main__':
    forca = Forca()
import pygame
from random import randint
from sys import exit

pygame.init()

class Forca:
    def __init__(self):
        self.SCREEN_X, self.SCREEN_Y = 480, 520
        self.screen = pygame.display.set_mode((self.SCREEN_X, self.SCREEN_Y))
        pygame.display.set_caption("Jogo da forca")

        self.clock = pygame.time.Clock()

        self.arquivo = open("palavras.txt", "r")
        self.random_num = randint(0, len(self.arquivo.readlines())-1)

        self.arquivo = open("palavras.txt", "r")
        self.palavra_sorteada = self.arquivo.readlines()[self.random_num]
        self.palavra_sorteada = self.palavra_sorteada[0:len(self.palavra_sorteada)-1]

        self.base_font = pygame.font.Font(None, 32)
        self.user_text = ""
        self.input_rect = pygame.Rect(self.SCREEN_X/2 - 140/2, 350, 140, 32)
        self.color = pygame.Color("white")

        print(self.palavra_sorteada)

        self.game_over = False
        self.jogo()


    def jogo(self):
        self.letras_corretas = []
        self.letras_erradas = []

        for letras_da_palavra in self.palavra_sorteada:
             self.letras_corretas.append("_ ")

        while not self.game_over:
            self.screen.fill((0, 0, 0))

            self.forca()

            self.draw(str(self.letras_corretas).strip("[]").replace("'", ""), 32, (255, 255, 255), self.SCREEN_X/2, 300)

            pygame.draw.rect(self.screen, self.color, self.input_rect, 2)
            self.text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
            self.screen.blit(self.text_surface, (self.SCREEN_X/2, self.input_rect.y + 5))

            self.events()

            pygame.display.update()
            pygame.display.flip()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    c = 0
                    for i in self.palavra_sorteada.upper():
                        if self.user_text.upper() == i.upper():
                            self.letras_corretas.insert(c, i)
                            self.letras_corretas.pop(c+1)
                        else: # --------------------- !!!!!!!!!!!!!!!!!!!!!!!!
                            self.letras_erradas.append(self.user_text)
                            if self.letras_erradas[c] == i:
                                self.letras_erradas.remove(i)
                            #print(self.letras_erradas)
                        c += 1
                    self.user_text = ""
                else:
                    self.user_text = event.unicode


    def draw(self, text, tam, color, x, y):
        self.fonte = pygame.font.Font(pygame.font.match_font("arial"), tam)
        self.obj = self.fonte.render(text, False, color)
        self.obj_rect = self.obj.get_rect()
        self.obj_rect.center = (x, y)
        self.screen.blit(self.obj, self.obj_rect)


    def forca(self):
        self.draw("|", 100, (255, 255, 255), 100, 100)
        self.draw("|", 100, (255, 255, 255), 100, 190)
        self.draw("_", 100, (255, 255, 255), 121, 15)
        self.draw("_", 100, (255, 255, 255), 168, 15)
        self.draw("|", 50, (255, 255, 255), 190, 80)
        self.draw("O", 50, (255, 255, 255), 190, 125)
        self.draw("|", 50, (255, 255, 255), 190, 160)
        self.draw("/", 50, (255, 255, 255), 185, 170)
        self.draw("\\", 50, (255, 255, 255), 195, 170)
        self.draw("/", 50, (255, 255, 255), 185, 200)
        self.draw("\\", 50, (255, 255, 255), 195, 200)



if __name__ == '__main__':
    forca = Forca()

