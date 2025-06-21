from numero import Numero
from datetime import datetime

class Fatura():

    def __init__(self, origem : Numero = None, valor_pacote_minutos : float = 0, valor_pacote_mensagem : float = 0, valor_total : float = 0,
                 emissao : datetime = None, status : str = '', mes_referencia : datetime = None, data_emissao : datetime = None):
        
        self.__origem = origem
        self.__valor_pacote_minutos = valor_pacote_minutos
        self.__valor_pacote_mensagem = valor_pacote_mensagem
        self.__valor_total = valor_total
        self.__emissao = emissao
        self.__status = status
        self.__mes_referencia = mes_referencia
        self.__data_emissao = data_emissao

    # encapsulamento aqui!
    # toda vez que alterar os valores de valor_pacote_min, irá alterar automaticamnete o valor_total