from .solicitacao import Solicitacao
from .usuario import Usuario
from .cliente import Cliente
from datetime import datetime

class Administrador(Usuario):
    def __init__(self, nome: str, cpf: str, email: str, senha: str, data_registro: datetime, banco):
        super().__init__(nome, cpf, email, senha, data_registro, 'administrador')
        self.solicitacoes = []