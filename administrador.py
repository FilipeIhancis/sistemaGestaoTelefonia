from solicitacao import Solicitacao
from usuario import Usuario
from cliente import Cliente
from BancoDeDados import BancoDeDados

class Administrador(Usuario):
    def __init__(self, id: str, solicitacoes: list[Solicitacao]):
        self.id = id
        self.solicitacoes = solicitacoes
    
    def listar_clientes(self) -> list[Cliente]:
        pass

    def alterar_plano_numero(self) -> None:
        pass

    def excluir_cliente(self, cliente: Cliente) -> None:
        pass

    def adicionar_numero_cliente(self, cliente: Cliente) -> None:
        pass
