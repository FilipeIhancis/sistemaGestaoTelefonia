from datetime import datetime

class Mensagem:

    def __init__(self, conteudo: str = '', origem: str = '', destino: str = '', data_envio: datetime = None):

        self.conteudo = conteudo
        self.origem = origem                # Objeto Numero
        self.destino = destino              # Número de destino como string
        self.data_envio = data_envio

    @property
    def conteudo(self):
        return self.__conteudo
    
    @conteudo.setter
    def conteudo(self, msg : str):
        if not isinstance(msg, str) or msg == '':
            raise ValueError
        self.__conteudo = msg

    @property
    def origem(self):
        return self.__origem
    
    @origem.setter
    def origem(self, numero_origem : str):
        if not isinstance(numero_origem, str):
            raise ValueError
        self.__origem = numero_origem

    @property
    def destino(self):
        return self.__destino
    
    @origem.setter
    def origem(self, numero_destino : str):
        if not isinstance(numero_destino, str) or numero_destino == '':
            raise ValueError
        self.__destino = numero_destino

    @property
    def data_envio(self):
        return self.__data_envio
    
    @data_envio.setter
    def data_envio(self, data : datetime):
        if not isinstance(data, datetime):
            raise ValueError
        self.__data_envio = data
    

    def calcular_custo(self) -> float:
        if not self.origem.assinatura or not self.origem.assinatura.plano:
            return 0.0
        return self.origem.assinatura.plano.preco_sms
