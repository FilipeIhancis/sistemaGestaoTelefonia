from database.BancoDeDados import BancoDeDados, T
from models import *
from datetime import datetime

class BancoSolicitacao(BancoDeDados[Usuario]):

    def __init__(self, diretorio : str = ''):
        super().__init__(diretorio)

    def salvar(self, solicitacao : Solicitacao) -> None:
        
        print('oi')