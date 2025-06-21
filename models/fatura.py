from datetime import datetime

class Fatura():

    def __init__(self, origem : str = '', valor_pacote_minutos : float = 0, valor_pacote_mensagem : float = 0, valor_total : float = 0,
                 emissao : datetime = None, status : str = '', mes_referencia : datetime = None, data_emissao : datetime = None):
        
        self.origem = origem
        self.valor_pacote_minutos = valor_pacote_minutos
        self.valor_pacote_mensagem = valor_pacote_mensagem
        self.valor_total = valor_total
        self.emissao = emissao
        self.status = status
        self.mes_referencia = mes_referencia
        self.data_emissao = data_emissao

    @property
    def origem(self) -> str:
        return self.__origem

    @origem.setter
    def origem(self, numero: str):
        if numero is not None and not isinstance(numero, str):
            raise ValueError("origem precisa ser um objeto da classe Numero ou None.")
        self.__origem = numero

    @property
    def valor_pacote_minutos(self) -> float:
        return self.__valor_pacote_minutos

    @valor_pacote_minutos.setter
    def valor_pacote_minutos(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise ValueError("valor_pacote_minutos precisa ser numérico.")
        self.__valor_pacote_minutos = float(valor)

    @property
    def valor_pacote_mensagem(self) -> float:
        return self.__valor_pacote_mensagem

    @valor_pacote_mensagem.setter
    def valor_pacote_mensagem(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise ValueError("valor_pacote_mensagem precisa ser numérico.")
        self.__valor_pacote_mensagem = float(valor)

    @property
    def valor_total(self) -> float:
        return self.__valor_total

    @valor_total.setter
    def valor_total(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise ValueError("valor_total precisa ser numérico.")
        self.__valor_total = float(valor)

    @property
    def emissao(self) -> datetime:
        return self.__emissao

    @emissao.setter
    def emissao(self, data: datetime):
        if data is not None and not isinstance(data, datetime):
            raise ValueError("emissao precisa ser um objeto datetime ou None.")
        self.__emissao = data

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, status: str):
        if not isinstance(status, str):
            raise ValueError("status precisa ser uma string.")
        self.__status = status

    @property
    def mes_referencia(self) -> datetime:
        return self.__mes_referencia

    @mes_referencia.setter
    def mes_referencia(self, mes: datetime):
        if mes is not None and not isinstance(mes, datetime):
            raise ValueError("mes_referencia precisa ser um objeto datetime ou None.")
        self.__mes_referencia = mes

    @property
    def data_emissao(self) -> datetime:
        return self.__data_emissao

    @data_emissao.setter
    def data_emissao(self, data: datetime):
        if data is not None and not isinstance(data, datetime):
            raise ValueError("data_emissao precisa ser um objeto datetime ou None.")
        self.__data_emissao = data


    # encapsulamento aqui!
    # toda vez que alterar os valores de valor_pacote_min, irá alterar automaticamnete o valor_total