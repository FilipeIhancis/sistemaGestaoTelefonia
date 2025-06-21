from cliente import Cliente
from assinatura import Assinatura
from ligacao import Ligacao
from mensagem import Mensagem
from BancoDeDados import BancoDeDados

class Numero:
    def __init__(self, numero: str, cliente_dono: Cliente, id_assinatura: int, banco: BancoDeDados):
        self.numero = numero
        self.cliente_dono = cliente_dono
        self.id_assinatura = id_assinatura
        self.banco = banco
        self.assinatura = self.banco.get_assinatura_por_id(id_assinatura)  # [BANCO] Criar método que retorna objeto Assinatura para esse ID
        self.ligacoes = self.banco.get_ligacoes_por_numero(numero)  # [BANCO] Criar método que retorna lista de Ligacao para esse número
        self.mensagens = self.banco.get_mensagens_por_numero(numero)  # [BANCO] Criar método que retorna lista de Mensagem para esse número

    def assinatura_ativa(self) -> bool:
        return self.assinatura.esta_ativa()

    def enviar_mensagem(self, numero_destino: str, conteudo: str) -> None:
        from datetime import datetime
        mensagem = Mensagem(conteudo, self, numero_destino, datetime.now())
        self.banco.registrar_mensagem(mensagem)  # [BANCO] Criar método para inserir a mensagem na tabela MENSAGENS
        self.mensagens.append(mensagem)

    def registrar_ligacao(self, numero_destino: str, duracao: int) -> None:
        from datetime import datetime, timedelta
        inicio = datetime.now()
        fim = inicio + timedelta(minutes=duracao)
        ligacao = Ligacao(self, numero_destino, duracao, inicio, fim)
        self.banco.registrar_ligacao(ligacao)  # [BANCO] Criar método para inserir a ligação na tabela LIGACOES
        self.ligacoes.append(ligacao)

    def get_ligacoes(self) -> list[Ligacao]:
        return self.ligacoes

    def get_mensagens(self) -> list[Mensagem]:
        return self.mensagens   
