from plano import Plano
from datetime import datetime

class Assinatura:
    def __init__(self, id_assinatura: int, plano: Plano, data_assinatura: datetime, ativa: bool):
        self.id_assinatura = id_assinatura
        self.plano = plano
        self.data_assinatura = data_assinatura
        self.ativa = ativa

    def desativar(self, banco) -> None:
        self.ativa = False
        banco.desativar_assinatura(self.id_assinatura)  # [BANCO] Criar método que atualiza o campo 'ativa' da assinatura para 'False'

    def esta_ativa(self) -> bool:
        return self.ativa

