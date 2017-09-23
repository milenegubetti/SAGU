"""
Este modulo define a classe Vetor
"""


class Vetor(object):
    """
    Esta classe representa um vetor bidimensional
    """

    def __init__(self, x, y):
        """
        Neste metodo um vetor e criado a partir de suas componentes x e y

        :param x: Componente x do vetor
        :param y: Componente y do vetor
        """

        self.posicao = (x, y)

    def __str__(self):
        """
        Este metodo retorna uma representacao textual de um vetor

        :return: String que representa o vetor atual
        """

        return "(%s, %s)" % self.posicao

    def __add__(self, v):
        """
        Este metodo soma dois vetores

        :param v: O vetor a que o vetor corrente sera somado
        :return: O vetor resultante da soma dos outros dois vetores
        """

        return Vetor(self.posicao[0] + v.posicao[0], self.posicao[1] + v.posicao[1])

    def __sub__(self, v):
        """
        Este metodo subtrai dois vetores

        :param v: O vetor que sera subtraido do vetor corrente
        :return: O vetor resultante do vetor corrente subtraido do vetor v
        """

        return Vetor(self.posicao[0] - v.posicao[0], self.posicao[1] - v.posicao[1])

    def __neg__(self):
        """
        Este metodo inverte o sentido de um vetor

        :return: O vetor inverso do vetor corrente
        """

        return Vetor(-self.posicao[0], -self.posicao[1])

    def __mul__(self, escalar):
        """
        Este metodo multiplica um vetor por um escalar

        :param escalar: Um numero real que multiplicara o vetor corrente
        :return: O vetor resultante da multiplicacao do vetor corrente pelo escalar
        """

        return Vetor(self.posicao[0] * escalar, self.posicao[1] * escalar)

    def __truediv__(self, escalar):
        """
        Este metodo divide um vetor por um escalar

        :param escalar: Um numero real que divide o vetor corrente
        :return: O vetor resultante da divisao do vetor corrente pelo escalar
        """
        try:
            return Vetor(self.posicao[0] / escalar, self.posicao[1] / escalar)
        except ZeroDivisionError:
            return self

    def modulo(self):
        """
        Este metodo encontra o modulo do vetor corrente

        :return: O modulo do vetor corrente
        """

        return (self.posicao[0] ** 2 + self.posicao[1] ** 2) ** (1 / 2)

    def normalizar(self):
        """
        Este metodo normaliza o vetor (deixa-o com a mesma direcao e sentido mas
        com modulo igual a 1)

        :return: Um vetor com a mesma direcao e sentido, mas com modulo 1
        """

        return self / self.modulo()

    def produto_escalar(self, v):
        """
        Este metodo encontra o produto escalar entre dois vetores

        :param v: O outro vetor que faz parte da operacao de produto escalar
        :return: O produto escalar entre os dois vetores
        """

        return self.posicao[0] * v.posicao[0] + self.posicao[1] * v.posicao[1]

    def get_tupla(self):
        """
        Este metodo retorna uma representacao do vetor em forma de tupla (x,y)

        :return: Uma tupla com os componentes x e y do vetor
        """

        return self.posicao
