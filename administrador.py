from solicitacao import Solicitacao
from usuario import Usuario
from cliente import Cliente
from BancoDeDados import BancoDeDados
from datetime import datetime

class Administrador(Usuario):
    def __init__(self, id: str, nome: str, cpf: str, email: str, senha: str, data_registro: datetime, banco: BancoDeDados):
        super().__init__(nome, cpf, email, senha, data_registro)
        self.id = id
        self.banco = banco
        self.solicitacoes = []  # [BANCO] No futuro: buscar solicitações pendentes atribuídas a este administrador

    def listar_clientes(self) -> list[Cliente]:
        return self.banco.get_clientes()  # [BANCO] Criar método que retorna lista de objetos Cliente (consultando USUARIO onde tipo='CLIENTE')

    def alterar_plano_numero(self, numero: str, novo_plano_id: int) -> None:
        self.banco.alterar_plano_do_numero(numero, novo_plano_id)  # [BANCO] Criar método que atualiza a assinatura do número para um novo plano

    def excluir_cliente(self, cliente: Cliente) -> None:
        self.banco.excluir_cliente(cliente.cpf)  # [BANCO] Criar método que exclui o cliente e seus dados vinculados

    def adicionar_numero_cliente(self, cliente: Cliente, numero: str, id_assinatura: int) -> None:
        self.banco.adicionar_numero(numero, cliente.cpf, id_assinatura)  # [BANCO] Já existe método de adicionar número
