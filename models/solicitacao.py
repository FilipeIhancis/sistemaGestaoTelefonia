from cliente import Cliente 
from datetime import datetime

class Solicitacao:
    def __init__(self, id_solicitacao: int, tipo: str, status: bool, cliente_solicitante: Cliente, data: datetime):
        self.id_solicitacao = id_solicitacao
        self.tipo = tipo                                    # Ex: "ALTERAR PLANO", "ADICIONAR NÚMERO"
        self.status = status                                # True = resolvida, False = pendente
        self.cliente_solicitante = cliente_solicitante
        self.data = data

    def finalizar_solicitacao(self, banco) -> None:
        self.status = True
        banco.marcar_solicitacao_como_concluida(self.id_solicitacao)  # [BANCO] Criar método para atualizar o status da solicitação para True

