"""
Este modulo define a classe Jogo
"""

import sys
from os import system

import pygame

from objeto import Objeto
from nave import Nave
from obstaculo import Obstaculo
from vetor import Vetor


class Jogo:
    """
    Esta classe controla o funcionamento de um jogo
    """
    lista_naves = []
    lista_objetos = []

    def __init__(self):
        """
        Neste metodo o ambiente pygame e criado
        """
        
        self.ambiente = pygame
        self.ambiente.init()

    def criar_tela(self, titulo, tamanho, background, flag=0):
        """
        Este metodo cria a tela do jogo, converte a imagem de fundo e converte
        as imagens dos objetos

        :param titulo: O titulo da tela do jogo
        :param tamanho: O tamanho da tela do jogo
        :param background: A string da imagem do plano de fundo do jogo
        :param flag: As flags da tela do jogo
        """
        
        self.ambiente.display.set_caption(titulo)
        self.tela = self.ambiente.display.set_mode(tamanho, flag, 32)
        
        self.background = pygame.image.load("Imagens/" + background + ".png").convert()
        for objeto in self.lista_objetos:
        	objeto.imagem.convert_alpha()

    def atualizar_tela(self):
        """
        Este metodo atualiza a tela
        """

        self.ambiente.display.flip()

    def desenhar_background(self):
        """
        Este metodo desenha o plano de fundo da tela
        """

        self.tela.blit(self.background, (0, 0))

    def adicionar_nave(self, nave):
        """
        Este metodo adiciona um nave no jogo

        :param nave: A nave que sera adicionado ao jogo
        """

        self.lista_naves.append(nave)

    def adicionar_objeto(self, objeto):
        """
        Este metodo adiciona um objeto no jogo

        :param objeto: O objeto que sera adicionado ao jogo
        """

        self.lista_objetos.append(objeto)

    def atualizar(self):
        """
        Este metodo atualiza todos os objetos do jogo
        Caso seja um Obstaculo, chama o metodo com um argumento lista_objetos
        """

        for objeto in self.lista_objetos:
            objeto.atualizar(self)

        for nave in self.lista_naves:
            nave.atualizar(self)
            for tiro in nave.lista_tiros:
                tiro.atualizar(self)

    def desenhar(self):
        """
        Este metodo desenha a barra de pontos de vida e todos os objetos do jogo
        """

        altura_tela, largura_tela = self.tela.get_height(), self.tela.get_width()
        
        try:
            altura_ponto = altura_tela / 100
        except:
            altura_ponto = 20

        for i in range(2):
            nave = self.lista_naves[i]
            
            pygame.draw.rect(self.tela, (192,192,192), (i*(largura_tela-16), altura_tela, 16, -nave.pontos_de_vida*altura_ponto) )
            nave.desenhar(self.ambiente, self.tela)
            
            for tiro in nave.lista_tiros:
                tiro.desenhar(self.tela)
        
        for objeto in self.lista_objetos:
            objeto.desenhar(self.tela)

    def tratar_eventos(self):
        """
        Este metodo trata os eventos do jogo
        """

        for event in self.ambiente.event.get():
            if event.type == self.ambiente.QUIT:
                sys.exit()
            if event.type == self.ambiente.USEREVENT+1:
                self.lista_naves[0].pode_atirar = True
            if event.type == self.ambiente.USEREVENT+2:
                self.lista_naves[1].pode_atirar = True
            if event.type == self.ambiente.USEREVENT+3:
                self.lista_naves[0].pode_colidir = True
            if event.type == self.ambiente.USEREVENT+4:
                self.lista_naves[1].pode_colidir = True

    def selecao(self):
        """
        Este metodo controla a selecao de jogadores e naves
        """
        for i in range(2):
            system("clear")
            print("SELEÇÃO")
            print("1 - Criar")
            print("2 - Já tenho")
            opcao = input(": ")

            if opcao == "1": 
                print("\nJOGADOR")
                while True:
                    nome = input("Nome: ").upper()

                    if not self.buscar_nome(nome):
                        break
                    else:
                        print("Este jogador já existe.\n")

                print("\nNAVE")
                print("Você tem 10 pontos para distribuir (entre velocidade máxima, aceleração e escudo).")

                while True:
                    try:
                        velocidade_maxima = int(input("Velocidade máxima (1-5): "))
                        aceleracao = int(input("Aceleração (1-5): "))
                        escudo = int(input("Escudo (0-5): "))
                    except:
                        print("Valor inválido!\n")
                        continue

                    if velocidade_maxima+aceleracao+escudo <= 10:
                        break
                    else:
                        print("Você gastou mais de 10 pontos.\n")

                while True:
                    print("Cor:")
                    print("1 - vermelho")
                    print("2 - amarelo")
                    print("3 - verde")
                    print("4 - azul turquesa")
                    print("5 - azul")
                    print("6 - roxo")

                    try:
                        cor = int(input(": "))
                    except:
                        print("Valor inválido!\n")
                        continue

                    if cor > 0 and cor < 7:
                        break
                    else:
                        print("Cor inexistente.")

                if i == 0:
                    nave = Nave(jogo.ambiente, cor, Vetor(200, 300), velocidade_maxima, aceleracao*0.5, escudo, 0)
                else:
                    nave = Nave(jogo.ambiente, cor, Vetor(1000, 300), velocidade_maxima, aceleracao*0.5, escudo, 1)
                self.lista_naves.append(nave)
                
                self.salvar_configuracao(nome, cor, velocidade_maxima, aceleracao*0.5, escudo)
                
            elif opcao == "2":
                nome = input("Nome: ").upper()

                configuracao = self.ler_configuracao(nome)

                if i == 0:
                    nave = Nave(jogo.ambiente, configuracao[0], Vetor(200, 300), configuracao[1], configuracao[2], configuracao[3], 0)
                else:
                    nave = Nave(jogo.ambiente, configuracao[0], Vetor(1000, 300), configuracao[1], configuracao[2], configuracao[3], 1)
                self.lista_naves.append(nave)

            else:
                print("Opção inválida")
                sys.exit()

    def salvar_configuracao(self, nome, cor, velocidade_maxima, aceleracao, escudo):
        """
        Este metodo salva a configuracao da nave num arquivo
        
        :param nome: O nome do jogador
        :param cor: A cor da nave
        :param velocidade_maxima: A velocidade maxima da nave
        :param aceleracao: A aceleracao da nave
        :param escudo: Os pontos de defesa da nave
        """
        
        arquivo = open("configuracoes.txt", "a")
        texto = [nome+"\n", str(cor)+";", str(velocidade_maxima)+";", str(aceleracao)+";", str(escudo)+"\n"]
        arquivo.writelines(texto)
        arquivo.close()            


    def ler_configuracao(self, nome):
        """
        Este metodo le as configuracoes de uma nave
        
        :param nome: O nome do jogador
        """
        
        arquivo = open("configuracoes.txt", "r")
        texto = arquivo.readlines()
        count = 0
        for linha in texto:
            if linha == nome+"\n":
                configuracao = texto[count+1].split(";")
            count += 1
        arquivo.close()
        try:
            return [int(configuracao[0]), int(configuracao[1]), float(configuracao[2]), int(configuracao[3])]
        except:
            return [0,3,3,3]

    def buscar_nome(self, nome):
        """
        Este metodo procura um jogador no arquivo das configuracoes
        
        :param nome: O nome do jogador
        """
        
        arquivo = open("configuracoes.txt", "r")
        texto = arquivo.readlines()
        for linha in texto:
            if linha == nome+"\n":
                return True
        return False

    def verificar_fim_do_jogo(self):
        """
        Este metodo verifica se o jogo acabou        
        """

        if self.lista_naves[0].pontos_de_vida <= 0:
            print("O jogador 2 venceu!")
            sys.exit()
        elif self.lista_naves[1].pontos_de_vida <= 0:
            print("O jogador 1 venceu!")
            sys.exit()

    def run(self):
        """
        Este metodo executa o loop de jogo
        """
        clock = self.ambiente.time.Clock()

        while True:
            self.verificar_fim_do_jogo()
            self.tratar_eventos()

            self.desenhar_background()

            self.atualizar()
            self.desenhar()

            self.atualizar_tela()

            clock.tick(60)


if __name__ == "__main__":
    jogo = Jogo()
    """
    nave1 = Nave(jogo.ambiente, 1, Vetor(200, 300), 6, 0.1, 1, 0)
    nave2 = Nave(jogo.ambiente, 2, Vetor(1000, 300), 3, 0.3, 1, 1)
    jogo.adicionar_nave(nave1)
    jogo.adicionar_nave(nave2)
    """
    jogo.selecao()

    asteroide1 = Obstaculo(jogo.ambiente, "asteroide_0", Vetor(600, 200), Vetor(1,0.35), 2)
    asteroide2 = Obstaculo(jogo.ambiente, "asteroide_0", Vetor(600, 400), Vetor(-1,-0.35), 2)
    asteroide3 = Obstaculo(jogo.ambiente, "asteroide_0", Vetor(600, 300), Vetor(0.0,0.1), 0.2)
    jogo.adicionar_objeto(asteroide1)
    jogo.adicionar_objeto(asteroide2)
    jogo.adicionar_objeto(asteroide3)

    jogo.criar_tela("Sagu", (1280, 720), "fundo")

    jogo.run()
