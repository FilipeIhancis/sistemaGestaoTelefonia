from datetime import datetime, timedelta


class Ligacao:

    def __init__(self, origem : str = '', destino: str = '', data_inicio: datetime = None, data_fim: datetime = None):

        self.origem = origem 
        self.destino = destino 
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.duracao = (self.data_inicio - self.data_fim).total_seconds()

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
    def destino(self, dest : str):
        if not isinstance(dest, str):
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
