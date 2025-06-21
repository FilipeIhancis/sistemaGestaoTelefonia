from usuario import Usuario
from numero import Numero
from database.BancoDeDados import BancoDeDados
from datetime import datetime

class Cliente(Usuario):
    def __init__(self, id: str, nome: str, cpf: str, email: str, senha: str, data_registro: datetime, banco: BancoDeDados):
        super().__init__(nome, cpf, email, senha, data_registro)
        self.id = id
        self.banco = banco
        self.numeros = self.banco.get_numeros_por_cliente(cpf)  # [BANCO] Criar método que retorne objetos Numero para o CPF informado

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
