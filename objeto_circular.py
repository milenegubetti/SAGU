#http://ericleong.me/research/circle-circle/
"""
Este modulo define uma classe ObjetoCircular
"""
from objeto import Objeto
from vetor import Vetor


class ObjetoCircular(Objeto):
    """
    Esta classe representa um objeto circular generico do jogo
    """

    def __init__(self, ambiente, imagem, posicao=Vetor(0, 0)):
        """
        Neste metodo um objeto circular e criado

        :param ambiente: O ambiente pygame do jogo, que e usado para carregar
                         a imagem
        :param imagem: O caminho da imagem do objeto
        :param posicao: A posicao inicial do objeto
        """

        Objeto.__init__(self, ambiente, imagem, posicao)

        self._raio = self.imagem.get_width() / 2
        self.posicao += Vetor(self._raio, self._raio)

    def desenhar(self, tela):
        """
        Este metodo desenha o objeto na tela

        :param tela: A tela onde o objeto sera desenhado
        """
        
        posicao_desenho = self.posicao - Vetor(self._raio, self._raio)

        tela.blit(self.imagem, posicao_desenho.get_tupla())

    def colidir_objetos(self, lista_objetos):
        """
        Este metodo checa a colisao do objeto corrente com todos os objetos da lista

        :param lista_objetos: A lista de objetos que sera checada a colisao
        :return: A lista dos objetos com os quais o objeto corrente colide
        """
        lista_colisoes = []

        for objeto in lista_objetos:
            if objeto is not self and self.colidir_circulo(objeto):
                lista_colisoes.append(objeto)

        return lista_colisoes

    def colidir_circulo(self, circulo):
        """
        Este metodo checa a colisao do objeto corrente com um circulo

        :param circulo: O circulo que sera checada a colisao
        """
        distancia = (circulo.posicao - self.posicao).modulo()
        
        if distancia < self._raio + circulo._raio:
            return True
        else:
            return False
