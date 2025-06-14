from datetime import datetime
from numero import Numero

class Mensagem(Numero):
    def __init__(self, conteudo: str, origem: Numero, destino: str, data_envio: datetime):
        self.conteudo = conteudo
        self.origem = origem
        self.destino = destino
        self.data_envio = data_envio
    
    def calcular_custo(self) -> float:
        pass


