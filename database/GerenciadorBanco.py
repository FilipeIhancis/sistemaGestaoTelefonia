from database.daos.BancoNumero import BancoNumero
from database.daos.BancoUsuario import BancoUsuario
from database.daos.BancoAssinatura import BancoAssinatura
from database.daos.BancoPlano import BancoPlano
from database.daos.BancoFatura import BancoFatura
from database.daos.BancoSolicitacao import BancoSolicitacao
from database.BancoDeDados import BancoDeDados
from models import *

class GerenciadorBanco:

    def __init__(self, diretorio : str = ''):
        self.numeros = BancoNumero(diretorio)
        self.usuarios = BancoUsuario(diretorio)
        self.assinaturas = BancoAssinatura(diretorio)
        self.planos = BancoPlano(diretorio)
        self.faturas = BancoFatura(diretorio)
        self.solicitacoes = BancoSolicitacao(diretorio)

    @property 
    def numeros(self):
        return self._numeros
    
    @numeros.setter
    def numeros(self, bancoNumeros : BancoDeDados):
        if not isinstance(bancoNumeros, BancoDeDados):
            raise ValueError
        self._numeros = bancoNumeros

    @property 
    def usuarios(self):
        return self._usuarios
    
    @usuarios.setter
    def usuarios(self, bancoUsuarios : BancoDeDados):
        if not isinstance(bancoUsuarios, BancoDeDados):
            raise ValueError
        self._usuarios = bancoUsuarios

    @property
    def assinaturas(self):
        return self._assinaturas
    
    @assinaturas.setter
    def assinaturas(self, bancoAssinaturas : BancoDeDados):
        if not isinstance(bancoAssinaturas, BancoDeDados):
            raise ValueError
        self._assinaturas = bancoAssinaturas
    
    @property
    def planos(self):
        return self._planos

    @planos.setter
    def planos(self, planoBancos : BancoDeDados):
        if not isinstance(planoBancos, BancoDeDados):
            raise ValueError
        self._planos = planoBancos
    
    @property
    def faturas(self):
        return self._faturas

    @faturas.setter
    def faturas(self, bancoFaturas : BancoDeDados):
        if not isinstance(bancoFaturas, BancoDeDados):
            raise ValueError
        self._faturas = bancoFaturas