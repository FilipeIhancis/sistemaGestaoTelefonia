from datetime import datetime
from numero import Numero

class Ligacao(Numero):
    def __init__(self, origem: Numero, destino: str, duracao: int, data_inicio: datetime, data_fim: datetime):
        self.origem = origem
        self.destino = destino
        self.duracao = duracao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
    
    def calcular_custo(self) -> float:
        pass


