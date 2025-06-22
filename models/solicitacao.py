from .usuario import Usuario
from datetime import datetime


class Solicitacao:

    def __init__(self, id : int = 1, categoria: str = '', status: bool = False, cliente_solicitante: Usuario = None, 
                 data: datetime = datetime.now(), assunto : str = '', observacoes : str = ''):

        self.id : int = id
        self.categoria : str = categoria
        self.status : bool = status
        self.cliente_solicitante : Usuario = cliente_solicitante
        self.data : datetime = data
        self.assunto : str = assunto
        self.observacoes : str = observacoes

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, novo_id : int):
        if not isinstance(novo_id, int) or novo_id < 0:
            raise ValueError("ID inválido")
        self.__id = novo_id

    @property
    def categoria(self) -> str:
        return self.__categoria
    
    @categoria.setter
    def categoria(self, nova_categoria : str) -> None:
        if not isinstance(nova_categoria, str):
            raise ValueError('Categoria inválida')
        self.__categoria = nova_categoria

    @property   
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, resolvida : bool) -> None:
        if not isinstance(resolvida, bool):
            raise ValueError('Tipo de status inválido')
        self.__status = resolvida

    @property
    def assunto(self) -> str:
        return self.__assunto
    
    @assunto.setter
    def assunto(self, novo_assunto:str) -> None:
        if not isinstance(novo_assunto, str):
            raise ValueError('Tipo de assunto inválido')
        self.__assunto = novo_assunto

    @property
    def cliente_solicitante(self) -> Usuario:
        return self.__cliente_solicitante
    
    @cliente_solicitante.setter
    def cliente_solicitante(self, cliente : Usuario):
        if not isinstance(cliente, Usuario):
            raise ValueError('Usuário inválido')
        self.__cliente_solicitante = cliente

    @property
    def observacoes(self) -> str:
        return self.__observacoes
    
    @observacoes.setter
    def observacoes(self, obs : str) -> None:
        if not isinstance(obs, str):
            raise ValueError
        self.__observacoes = obs