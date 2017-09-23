"""
Este modulo define uma classe ObjetoMovel, que e um objeto que pode se mover na tela
"""
from objeto import Objeto
from vetor import Vetor


class ObjetoMovel(Objeto):
    """
    Esta classe representa um objeto movel generico do jogo
    """

    def __init__(self, ambiente, imagem, posicao=Vetor(0,0), direcao=Vetor(0,0), velocidade=0):
        """
        Neste metodo um objeto movel e criado

        :param ambiente: O ambiente pygame do jogo, que e usado para carregar
                         a imagem
        :param imagem: O caminho da imagem do objeto
        :param posicao: A posicao inicial do objeto
        :param direcao: A direcao inicial do objeto
        :param velocidade: A velocidade inicial do objeto
        """

        Objeto.__init__(self, ambiente, imagem, posicao)

        self.direcao = direcao
        self.velocidade = velocidade

    def atualizar(self):
        """
        Este metodo atualiza a posicao do objeto de acordo com a sua direcao
        e velocidade
        """

        self.posicao += self.direcao * self.velocidade


    def adicionar_movimento(self, movimento):
        """
        Este metodo adiciona um vetor movimento ao objeto, o que pode alterar
        sua direcao e velocidade

        :param movimento: O vetor que sera adicionado ao movimento do objeto
        """
        vetor = ((self.direcao*self.velocidade)+movimento)
        self.velocidade = vetor.modulo()
        self.direcao = vetor.normalizar()

