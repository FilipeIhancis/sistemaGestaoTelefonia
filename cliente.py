from usuario import Usuario
from numero import Numero
from BancoDeDados import BancoDeDados

class Cliente(Usuario):
    def __init__(self, id: str, numeros: list[Numero]):
        self.id = id
        self.numeros = numeros
    
    def visualizar_numeros(self) -> None:
        pass

    def visualizar_ligacoes(self) -> None:
        pass

    def ver_mensagens(self) -> None:
        pass
