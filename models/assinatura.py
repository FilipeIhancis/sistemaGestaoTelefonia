from .plano import Plano
from datetime import datetime

class Assinatura:

    def __init__(self, plano: Plano, data_assinatura: datetime, ativa : bool = False):
        self.plano = plano
        self.data_assinatura = data_assinatura
        self.ativa = ativa

    @property
    def plano(self):
        return self.__plano
    
    @plano.setter
    def plano(self, plan : Plano):
        if not isinstance(plan, Plano):
            raise ValueError('plano precisa ser um objeto Plano')
        self.__plano = plan

    @property
    def data_assinatura(self) -> datetime:
        return self.__data_assinatura

    @data_assinatura.setter
    def data_assinatura(self, data: datetime):
        if not isinstance(data, datetime):
            raise ValueError("data_assinatura precisa ser um objeto datetime.")
        self.__data_assinatura = data

    @property
    def ativa(self) -> bool:
        return self.__ativa

    @ativa.setter
    def ativa(self, status: bool):
        if not isinstance(status, bool):
            raise ValueError("ativa precisa ser um valor booleano.")
        self.__ativa = status
    
    def desativar(self, banco) -> None:
        self.ativa = False
        #banco.desativar_assinatura(self.id_assinatura)  # [BANCO] Criar método que atualiza o campo 'ativa' da assinatura para 'False'

    def esta_ativa(self) -> bool:
        return self.ativa