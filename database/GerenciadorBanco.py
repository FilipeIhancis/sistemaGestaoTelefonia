from database.daos.BancoNumero import BancoNumero
from database.daos.BancoUsuario import BancoUsuario

class GerenciadorBanco:

    def __init__(self, diretorio : str = ''):

        self.numeros = BancoNumero(diretorio)
        self.usuarios = BancoUsuario(diretorio)