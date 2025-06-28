from .solicitacao import Solicitacao
from .usuario import Usuario
from datetime import datetime
import random


class Administrador(Usuario):

    def __init__(self, nome: str = '', cpf : str = '', email: str = '', senha: str = '', data_registro: datetime = datetime.now()):
        super().__init__(nome, cpf, email, senha, data_registro, 'ADMINISTRADOR')
        self.solicitacoes = []
        
    @property
    def solicitacoes(self):
        return self._solicitacoes
    
    @solicitacoes.setter
    def solicitacoes(self, novasSolicitacoes : Solicitacao):
        if not isinstance(novasSolicitacoes, Solicitacao) and not (isinstance(novasSolicitacoes, list) and all(isinstance(s, Solicitacao) for s in novasSolicitacoes)):
            raise ValueError("Solicitações do administrador inválidas.")
        self._solicitacoes = novasSolicitacoes

    def gerar_senha_aleatoria(self, tamanho : int = 5) -> str:

        if tamanho < 4:
            raise ValueError("O tamanho da senha deve ser de pelo menos 4 caracteres.")
        
        letras = 'abcdefghjkmnpqrstuvwxyz'  # sem i, l, o
        letras_maiusculas = 'ABCDEFGHJKMNPQRSTUVWXYZ'  # sem I, L, O
        digitos = '23456789'  # sem 0 e 1
        caracteres = letras + letras_maiusculas + digitos
        return ''.join(random.choices(caracteres, k=tamanho))