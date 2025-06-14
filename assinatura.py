from plano import Plano
from datetime import datetime

class Assinatura:
    def __init__(self, plano: Plano, data_assinatura: datetime, ativa: bool):
        self.plano = plano
        self.data_assinatura = data_assinatura
        self.ativa = ativa
    
    def desativar(self) -> None:
        pass

    def esta_ativa(self) -> bool:
        pass


