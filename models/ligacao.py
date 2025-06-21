from datetime import datetime, timedelta
from numero import Numero

class Ligacao:

    def __init__(self, origem : str = '', destino: Numero = None, data_inicio: datetime = None, data_fim: datetime = None):
        self.__origem = origem 
        self.__destino = destino 
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.__duracao = self.__data_inicio - self.__data_fim

    @property
    def origem(self):
        return self.__origem
    
    @origem.setter
    def origem(self, orig : str):
        if not isinstance(orig, str):
            raise ValueError
        self.__origem = orig

    @property
    def destino(self):
        return self.__destino

    @destino.setter
    def destino(self, dest : Numero):
        if not isinstance(dest, Numero):
            raise ValueError
        self.__destino = dest

    @property
    def duracao(self):
        self.__duracao

    @duracao.setter
    def duracao(self, dur : timedelta):
        if not isinstance(dur, timedelta):
            raise ValueError
        self.__duracao = dur
        

    def calcular_custo(self) -> float:
        if not self.origem.assinatura or not self.origem.assinatura.plano:
            return 0.0
        plano = self.origem.assinatura.plano
        if self.duracao <= plano.minutos_max_ligacao:
            return 0.0
        minutos_excedentes = self.duracao - plano.minutos_max_ligacao
        return minutos_excedentes * plano.custo_minuto_excedente()  # [BANCO] Definir ou calcular o custo por minuto excedente no plano
