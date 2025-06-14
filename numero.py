from cliente import Cliente
from assinatura import Assinatura
from ligacao import Ligacao
from mensagem import Mensagem

class Numero:
    def __init__(self, cliente_dono: Cliente, numero: str, assinaturas: Assinatura, ligacoes: list[Ligacao], mensagens: list[Mensagem]):
        self.cliente_dono = cliente_dono
        self.numero = numero
        self.assinaturas = assinaturas
        self.ligacoes = ligacoes
        self.mensagens = mensagens
    
    def assinatura_ativa() -> None:
        pass

    def enviar_mensagem(numero_destino: str) -> None:
        pass

    def registrar_ligacao() -> None:
        pass
    