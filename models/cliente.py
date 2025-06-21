from .usuario import Usuario
from .numero import Numero
from datetime import datetime

class Cliente(Usuario):

    def __init__(self, nome: str, cpf: str, email: str, senha: str, data_registro: datetime, numeros : list[Numero]):
        super().__init__(nome, cpf, email, senha, data_registro)
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

'''
    def visualizar_numeros(self) -> list[str]:
        return [numero.numero for numero in self.numeros]

    def visualizar_ligacoes(self) -> list[dict]:
        resultado = []
        for numero in self.numeros:
            ligacoes = numero.get_ligacoes()  # [BANCO] Criar método em Numero que use banco para retornar as ligações do número
            for lig in ligacoes:
                resultado.append({
                    "numero_origem": numero.numero,
                    "destino": lig.destino,
                    "data_inicio": lig.data_inicio,
                    "duracao": lig.duracao,
                    "custo": lig.calcular_custo()
                })
        return resultado

    def ver_mensagens(self) -> list[dict]:
        resultado = []
        for numero in self.numeros:
            mensagens = numero.get_mensagens()  # [BANCO] Criar método em Numero que use banco para retornar as mensagens do número
            for msg in mensagens:
                resultado.append({
                    "numero_origem": numero.numero,
                    "destino": msg.destino,
                    "conteudo": msg.conteudo,
                    "data_envio": msg.data_envio
                })
        return resultado
'''