

class Plano:
    def __init__(self, nome : str = '', dados_mb : int = 0, preco : float = 0.0, maximo_mensagens : int = 0, maximo_ligacao : int = 0,
                 minutos_max_ligacao : int = 0, pacote_mensagem_unitario : float = 0.0, pacote_minutos_unitario : float = 0.0):
        
        self.nome : str = nome
        self.dados_mb : int = dados_mb
        self.preco : float = preco
        self.maximo_mensagens : int = maximo_mensagens
        self.maximo_ligacao : int = maximo_ligacao
        self.minutos_max_ligacao : int = minutos_max_ligacao
        self.pacote_mensagem_unitario : float = pacote_mensagem_unitario
        self.pacote_minutos_unitario : float = pacote_minutos_unitario

    @property
    def nome(self) -> str:
        return self.__nome
    @nome.setter
    def nome(self, novo_nome:str) -> None:
        if not isinstance(novo_nome, str):
            raise ValueError
        self.__nome = novo_nome

    @property
    def dados_mb(self):
        return self.__dados_mb
    @dados_mb.setter
    def dados_mb(self, dados : int):
        if not isinstance(dados, int):
            raise ValueError
        self.__dados_mb = dados

    @property
    def preco(self):
        return self.__preco
    @preco.setter
    def preco(self, preco : float):
        if not isinstance(preco, float) and not isinstance(preco, int):
            raise ValueError
        self.__dados_mb = float(preco)
    
    @property
    def maximo_mensagens(self):
        return self.__maximo_mensagens
    @maximo_mensagens.setter
    def maximo_mensagens(self, max_msg : int):
        if not isinstance(max_msg, int):
            raise ValueError
        self.__maximo_mensagens = max_msg

    @property
    def maximo_ligacao(self):
        return self.__maximo_ligacao
    @maximo_ligacao.setter
    def maximo_ligacao(self, max_lig : int):
        if not isinstance(max_lig, int):
            raise ValueError
        self.__maximo_ligacao = max_lig

    @property
    def minutos_max_ligacao(self):
        return self.__minutos_max_ligacao
    @minutos_max_ligacao.setter
    def minutos_max_ligacao(self, min_max_lig : int):
        if not isinstance(min_max_lig, int):
            raise ValueError
        self.__minutos_max_ligacao = min_max_lig

    @property
    def pacote_mensagem_unitario(self):
        return self.__pacote_mensagem_unitario
    @pacote_mensagem_unitario.setter
    def pacote_mensagem_unitario(self, pacote : float):
        if not isinstance(pacote, float) and not isinstance(pacote, int):
            raise ValueError
        self.__pacote_mensagem_unitario = pacote

    @property
    def pacote_minutos_unitario(self):
        return self.__pacote_minutos_unitario
    @pacote_minutos_unitario.setter
    def pacote_minutos_unitario(self, pacote : float):
        if not isinstance(pacote, float) and not isinstance(pacote, int):
            raise ValueError
        self.__pacote_minutos_unitario = pacote
    

    def custo_minuto_excedente(self) -> float:
        # Custo do minuto extra baseado no valor médio por minuto, com acréscimo
        return (self.preco / self.minutos_max_ligacao) * 1.5  # Pode ajustar esse fator se quiser