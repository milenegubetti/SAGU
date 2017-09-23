"""
Este modulo define uma classe Obstaculo
"""
from objeto_movel import ObjetoMovel
from objeto_circular import ObjetoCircular
from vetor import Vetor


class Obstaculo(ObjetoMovel, ObjetoCircular):
    """
    Esta classe representa um obstaculo do jogo
    """

    def __init__(self, ambiente, imagem, posicao=Vetor(0,0), direcao=Vetor(0,0), velocidade=0, dano=20):
        """
        Neste metodo um obstaculo e criado

        :param ambiente: O ambiente pygame do jogo, que e usado para carregar
                         a imagem
        :param imagem: O caminho da imagem do obstaculo
        :param posicao: A posicao inicial do obstaculo
        :param direcao: A direcao inicial do obstaculo
        :param velocidade: A velocidade inicial do obstaculo
        """

        ObjetoMovel.__init__(self, ambiente, imagem, posicao, direcao, velocidade)
        ObjetoCircular.__init__(self, ambiente, imagem, posicao)

    def atualizar(self, jogo):
        """
        Este metodo atualiza a posicao do obstaculo de acordo com a sua direcao
        e velocidade, mas vai lentamente sendo "freiado"
        Este metodo tambem checa as colisoes do obstaculo

        :param jogo: O jogo no qual o objeto está
        """

        posicao = self.posicao.get_tupla()
        tamanho = jogo.tela.get_size()

        if (posicao[0]+self._raio < 0 or
              posicao[0]-self._raio > tamanho[0] or
              posicao[1]+self._raio < 0 or 
              posicao[1]-self._raio > tamanho[1]):

            del(self)
            return

        # COLISAO COM OBSTACULOS
        lista_colisoes = self.colidir_objetos(jogo.lista_objetos)
        if len(lista_colisoes) != 0:
            for objeto in lista_colisoes:
                normal = (self.posicao - objeto.posicao).normalizar()
                self.adicionar_movimento(normal)
                objeto.adicionar_movimento(-normal)

        # CHECA COLISAO COM OS TIROS DA NAVE 1
        lista_colisoes = self.colidir_objetos(jogo.lista_naves[0].lista_tiros)
        if len(lista_colisoes) != 0:
            for tiro in lista_colisoes:
                self.adicionar_movimento(tiro.direcao*0.1)
                jogo.lista_naves[0].lista_tiros.remove(tiro)

        # CHECA COLISAO COM OS TIROS DA NAVE 2
        lista_colisoes = self.colidir_objetos(jogo.lista_naves[1].lista_tiros)
        if len(lista_colisoes) != 0:
            for tiro in lista_colisoes:
                self.adicionar_movimento(tiro.direcao*0.1)

                jogo.lista_naves[1].lista_tiros.remove(tiro)


        if self.velocidade > 0.1:
            self.velocidade -= 0.002

        self.posicao += self.direcao * self.velocidade
