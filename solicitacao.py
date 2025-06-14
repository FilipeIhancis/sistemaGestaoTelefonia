from cliente import Cliente 
from datetime import datetime

class Solicitacao(Cliente):
    def __init__(self, tipo: str, status: bool, cliente_solicitante: Cliente, data: datetime):
        self.tipo = tipo
        self.status = status
        self.cliente_solicitante = cliente_solicitante
        self.data = data
    
    def finalizar_solicitacao(self) -> None:
        pass

