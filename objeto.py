"""
Este modulo define uma classe Objeto
"""
from vetor import Vetor


class Objeto(object):
    """
    Esta classe representa um objeto generico do jogo
    """

    def __init__(self, ambiente, imagem, posicao=Vetor(0,0)):
        """
        Neste metodo um objeto e criado

        :param ambiente: O ambiente pygame do jogo, que e usado para carregar
                         a imagem
        :param imagem: O caminho da imagem do objeto
        :param posicao: A posicao inicial do objeto
        """

        self.imagem = ambiente.image.load("Imagens/" + imagem + ".png")

        self.posicao = posicao

    def desenhar(self, tela):
        """
        Este metodo desenha o objeto na tela

        :param tela: A tela onde o objeto sera desenhado
        """

        tela.blit(self.imagem, self.posicao.get_tupla())

    def atualizar(self):
        """
        Este metodo atualiza o objeto
        Pode ser sobrescrito por uma subclasse
        """

        pass
