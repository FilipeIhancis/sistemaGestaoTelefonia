from datetime import datetime
from numero import Numero

class Ligacao:
    def __init__(self, origem: Numero, destino: str, duracao: int, data_inicio: datetime, data_fim: datetime):
        self.origem = origem 
        self.destino = destino 
        self.duracao = duracao  
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def calcular_custo(self) -> float:
        if not self.origem.assinatura or not self.origem.assinatura.plano:
            return 0.0
        plano = self.origem.assinatura.plano
        if self.duracao <= plano.minutos_max_ligacao:
            return 0.0
        minutos_excedentes = self.duracao - plano.minutos_max_ligacao
        return minutos_excedentes * plano.custo_minuto_excedente()  # [BANCO] Definir ou calcular o custo por minuto excedente no plano
