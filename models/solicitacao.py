from .cliente import Cliente 
from datetime import datetime


class Solicitacao:

    def __init__(self, categoria: str = '', status: bool = False, cliente_solicitante: Cliente = None, data: datetime = None, assunto : str = ''):

        self.categoria : str = categoria                                    # Ex: "ALTERAR PLANO", "ADICIONAR NÚMERO"
        self.status : bool = status                                # True = resolvida, False = pendente
        self.cliente_solicitante : Cliente = cliente_solicitante
        self.data : datetime = data
        self.assunto : str = assunto

    @property
    def categoria(self) -> str:
        return self.__categoria
    
    @categoria.setter
    def categoria(self, nova_categoria : str) -> None:
        if not isinstance(nova_categoria, str):
            raise ValueError
        self.__categoria = nova_categoria

    @property   
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, resolvida : bool) -> None:
        if not isinstance(resolvida, bool):
            raise ValueError
        self.__status = resolvida

    @property
    def assunto(self) -> str:
        return self.__assunto
    
    @assunto.setter
    def assunto(self, novo_assunto:str) -> None:
        if not isinstance(novo_assunto, str) or novo_assunto == '':
            raise ValueError
        self.__assunto = novo_assunto

    @property
    def cliente_solicitante(self) -> Cliente:
        return self.__cliente_solicitante
    
    @cliente_solicitante.setter
    def cliente_solicitante(self, cliente : Cliente):
        if not isinstance(cliente, Cliente):
            raise ValueError
        self.__cliente_solicitante = cliente

    def finalizar_solicitacao(self, banco) -> None:
        self.status = True
        banco.marcar_solicitacao_como_concluida(self.id_solicitacao)  # [BANCO] Criar método para atualizar o status da solicitação para True

