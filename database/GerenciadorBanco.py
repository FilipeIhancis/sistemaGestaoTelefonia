from database.daos.BancoNumero import BancoNumero
from database.daos.BancoUsuario import BancoUsuario
from database.daos.BancoAssinatura import BancoAssinatura
from database.daos.BancoPlano import BancoPlano
from database.daos.BancoFatura import BancoFatura
from models import *

class GerenciadorBanco:

    def __init__(self, diretorio : str = ''):

        self.numeros = BancoNumero(diretorio)
        self.usuarios = BancoUsuario(diretorio)
        self.assinaturas = BancoAssinatura(diretorio)
        self.planos = BancoPlano(diretorio)
        self.faturas = BancoFatura(diretorio)