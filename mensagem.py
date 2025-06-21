from datetime import datetime
from numero import Numero

class Mensagem:
    def __init__(self, conteudo: str, origem: Numero, destino: str, data_envio: datetime):
        self.conteudo = conteudo
        self.origem = origem  # Objeto Numero
        self.destino = destino  # Número de destino como string
        self.data_envio = data_envio

    def calcular_custo(self) -> float:
        if not self.origem.assinatura or not self.origem.assinatura.plano:
            return 0.0
        return self.origem.assinatura.plano.preco_sms
