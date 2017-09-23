"""
Este modulo define uma classe Nave
"""
import math
from objeto_movel import ObjetoMovel
from objeto_circular import ObjetoCircular
from obstaculo import Obstaculo
from vetor import Vetor


class Nave(ObjetoMovel, ObjetoCircular):
    """
    Esta classe representa uma nave do jogo
    """

    def __init__(self, ambiente, cor, posicao, velocidade_maxima, aceleracao, escudo, codigo):
        """
        Neste metodo uma nave e criada

        :param ambiente: O ambiente pygame do jogo, que e usado para carregar
                         a imagem
        :param cor: A cor da nave (numero de 0 a 5)
        :param posicao: A posicao inicial da nave
        :param velocidade_maxima: A velocidade maxima que a nave pode atingir
        :param aceleracao: A aceleracao que a nave possui
        :param escudo: A defesa da nave, que reduz o dano recebido
        """

        ObjetoMovel.__init__(self, ambiente, "nave_"+str(cor), posicao, Vetor(0,0), 0)
        ObjetoCircular.__init__(self, ambiente, "nave_"+str(cor), posicao)

        self.imagem_inicial = self.imagem

        self.pontos_de_vida = 100

        self.velocidade_maxima = velocidade_maxima
        self.aceleracao = aceleracao
        self.escudo = escudo

        self.codigo = codigo
        self.cor = cor
        self.pode_atirar = True
        self.pode_colidir = True

        self.angulo = 90

        self.lista_tiros = []


    def atualizar(self, jogo):
        """
        Este metodo atualiza a nave, reduzindo gradualmente sua velocidade,
        checando suas colisoes, movendo e tratando os seus eventos
        """

        if self.velocidade > 0.1:
            self.velocidade -= 0.005

        self.colidir(jogo)
        self.movimentar(jogo)
        self.tratar_eventos(jogo)
        
    def colidir(self, jogo):
        """
        Este metodo checa as colisoes da nave com outros objetos e faz a nave
        responder a elas

        :param jogo: O jogo no qual a nave esta
        """
        
        # COLISAO COM A OUTRA NAVE
        nave = jogo.lista_naves[1]
        if self.codigo == 0 and self.colidir_circulo(nave) and self.pode_colidir:
            self.pode_colidir = False
            nave.pode_colidir = False
            jogo.ambiente.time.set_timer(jogo.ambiente.USEREVENT + 3, 200)
            jogo.ambiente.time.set_timer(jogo.ambiente.USEREVENT + 4, 200)

            self.pontos_de_vida -= 15-self.escudo
            nave.pontos_de_vida -= 15-nave.escudo

            normal = (self.posicao - nave.posicao).normalizar()
            self.adicionar_movimento(normal*3)
            nave.adicionar_movimento(-normal*3)


        # COLISAO COM OS TIROS DA OUTRA NAVE
        if self.codigo == 0:
            lista_colisoes = self.colidir_objetos(jogo.lista_naves[1].lista_tiros)
            if len(lista_colisoes) != 0:
                for tiro in lista_colisoes:
                    self.pontos_de_vida -= 10-self.escudo
                    self.adicionar_movimento(tiro.direcao*0.3)
                    jogo.lista_naves[1].lista_tiros.remove(tiro)
        elif self.codigo == 1:
            lista_colisoes = self.colidir_objetos(jogo.lista_naves[0].lista_tiros)
            if len(lista_colisoes) != 0:
                for tiro in lista_colisoes:
                    self.pontos_de_vida -= 10-self.escudo
                    self.adicionar_movimento(tiro.direcao*0.3)
                    jogo.lista_naves[0].lista_tiros.remove(tiro)


        # COLISAO COM OBSTACULOS
        lista_colisoes = self.colidir_objetos(jogo.lista_objetos)
        if len(lista_colisoes) != 0:
            for objeto in lista_colisoes:
                if self.pode_colidir:
                    self.pode_colidir = False

                    if self.codigo == 0:
                        jogo.ambiente.time.set_timer(jogo.ambiente.USEREVENT + 3, 200)
                    elif self.codigo == 1:
                        jogo.ambiente.time.set_timer(jogo.ambiente.USEREVENT + 4, 200)

                    self.pontos_de_vida -= 20-self.escudo

                normal = (self.posicao - objeto.posicao).normalizar()
                self.adicionar_movimento(normal*2)
                objeto.adicionar_movimento(-normal)

    def movimentar(self, jogo):
        """
        Este metodo faz a nave se movimentar, impede que ela se movimente alem
        de sua velocidade maxima e impede que ela saia da tela

        :param jogo: O jogo no qual a nave esta
        """

        nova_posicao = (self.posicao + (self.direcao * self.velocidade)).get_tupla()
        tamanho = jogo.tela.get_size()

        if self.velocidade >= self.velocidade_maxima:
            self.velocidade = self.velocidade_maxima

        if (nova_posicao[0]-self._raio > 0 and
            nova_posicao[0]+self._raio < tamanho[0] and
            nova_posicao[1]-self._raio > 0 and
            nova_posicao[1]+self._raio < tamanho[1]):

            self.posicao = Vetor(nova_posicao[0], nova_posicao[1])

    def tratar_eventos(self, jogo):
        """
        Este metodo trata os eventos de pressionamento de teclas

        :param jogo: O jogo no qual a nave esta
        """

        teclas = jogo.ambiente.key.get_pressed()

        if self.codigo == 0:
            # FAZ A NAVE ATIRAR
            if teclas[jogo.ambiente.K_LSHIFT] and self.pode_atirar:
                direcao = Vetor(math.cos(self.angulo * math.pi/180),
                                -math.sin(self.angulo * math.pi/180))

                tiro = Obstaculo(jogo.ambiente, "tiro_"+str(self.cor),
                    self.posicao+(direcao*self._raio), direcao, 5, 5)

                self.lista_tiros.append(tiro)

                self.pode_atirar = False
                jogo.ambiente.time.set_timer(jogo.ambiente.USEREVENT + 1, 300)

            # ACELERA A NAVE
            if teclas[jogo.ambiente.K_w]:
                movimento_x = self.aceleracao * math.cos(self.angulo * math.pi/180)
                movimento_y = (-self.aceleracao) * math.sin(self.angulo * math.pi/180)
                self.adicionar_movimento(Vetor(movimento_x, movimento_y))

            # FREIA A NAVE
            elif teclas[jogo.ambiente.K_s]:
                movimento_x = (-self.aceleracao/2) * math.cos(self.angulo * math.pi/180)
                movimento_y = self.aceleracao/2 * math.sin(self.angulo * math.pi/180)
                self.adicionar_movimento(Vetor(movimento_x, movimento_y))

            # GIRA A NAVE NO SENTIDO ANTI-HORARIO
            if teclas[jogo.ambiente.K_a]:
                self.angulo += 2
                if self.angulo >= 360:
                    self.angulo = 0
            # GIRA A NAVE NO SENTIDO HORARIO
            elif teclas[jogo.ambiente.K_d]:
                self.angulo -= 2
                if self.angulo >= 360:
                    self.angulo = 0

        elif self.codigo == 1:
            # FAZ A NAVE ATIRAR
            if teclas[jogo.ambiente.K_RSHIFT] and self.pode_atirar:
                direcao = Vetor(math.cos(self.angulo * math.pi/180),
                                -math.sin(self.angulo * math.pi/180))

                tiro = Obstaculo(jogo.ambiente, "tiro_"+str(self.cor),
                    self.posicao+(direcao*self._raio), direcao, 5, 5)

                self.lista_tiros.append(tiro)

                self.pode_atirar = False
                jogo.ambiente.time.set_timer(jogo.ambiente.USEREVENT + 2, 300)

            # ACELERA A NAVE
            if teclas[jogo.ambiente.K_UP]:
                movimento_x = self.aceleracao * math.cos(self.angulo * math.pi/180)
                movimento_y = (-self.aceleracao) * math.sin(self.angulo * math.pi/180)
                self.adicionar_movimento(Vetor(movimento_x, movimento_y))

            # FREIA A NAVE
            elif teclas[jogo.ambiente.K_DOWN]:
                movimento_x = (-self.aceleracao/4) * math.cos(self.angulo * math.pi/180)
                movimento_y = (self.aceleracao/4) * math.sin(self.angulo * math.pi/180)
                self.adicionar_movimento(Vetor(movimento_x, movimento_y))

            # GIRA A NAVE NO SENTIDO ANTI-HORARIO
            if teclas[jogo.ambiente.K_LEFT]:
                self.angulo += 2
                if self.angulo >= 360:
                    self.angulo = 0

            # GIRA A NAVE NO SENTIDO HORARIO
            elif teclas[jogo.ambiente.K_RIGHT]:
                self.angulo -= 2
                if self.angulo >= 360:
                    self.angulo = 0

    def desenhar(self, ambiente, tela):
        """
        Este metodo desenha a nave na tela, com a sua posicao e rotacao

        :param ambiente: O ambiente Pygame em que a nave esta
        :param tela: A tela no qual a nave sera desenhada
        """

        self.imagem = ambiente.transform.rotate(self.imagem_inicial, self.angulo)
        largura, altura = self.imagem.get_size()
        posicao_de_desenho = self.posicao - Vetor(largura/2, altura/2)
        tela.blit(self.imagem, posicao_de_desenho.get_tupla())
