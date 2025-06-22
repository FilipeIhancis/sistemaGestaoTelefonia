from .usuario import Usuario
from .numero import Numero
from datetime import datetime

class Cliente(Usuario):

    def __init__(self, nome: str, cpf: str, email: str, senha: str, data_registro: datetime, numeros : list[Numero]):
        super().__init__(nome, cpf, email, senha, data_registro, 'cliente')
        self.numeros = numeros

    
    @property
    def numeros(self):
        return self.__numeros
    
    @numeros.setter
    def numeros(self, lista_numeros : list[Numero] = None):
        for num in lista_numeros:
            if not isinstance(num, Numero):
                raise ValueError
        self.__numeros = lista_numeros