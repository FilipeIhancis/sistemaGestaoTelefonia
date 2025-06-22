from database.BancoDeDados import BancoDeDados, T
from typing import List, Optional
from models import *

class BancoNumero(BancoDeDados[Numero]):

    def __init__(self, diretorio : str = ''):
        super().__init__(diretorio)


    def salvar(self, numero : Numero) -> None: 

        if self.numero_existe(numero.numero):
            print("Número já está cadastrado no banco de dados")
            return

        self.executar(
            """
            INSERT INTO NUMEROS_TELEFONE (numero, saldo, cpf_cliente)
            VALUES (?, ?, ?)
            """,
            (numero.numero, numero.saldo, numero.cpf_proprieatario)
        )


    def buscar_por_cpf(self, cpf_cliente : str = '') -> List[Numero]:

        resultados: List[Numero] = []

        linhas = self.executar_select(
            """
            SELECT numero, saldo, cpf_cliente, id_assinatura FROM NUMEROS_TELEFONE
            WHERE cpf_cliente = ?
            """,
            (cpf_cliente,)
        )

        if linhas:
            for linha in linhas:
                num = Numero(
                    numero=linha[0],
                    cpf_proprieatario=linha[2],
                    saldo=linha[1],
                    assinatura=None  # Se quiser, você pode depois buscar o plano relacionado usando o id_assinatura
                )
                resultados.append(num)

        return resultados
    
    
    def numero_existe(self, numero : str) -> bool:

        linhas = self.executar_select(
            """
            SELECT 1 FROM NUMEROS_TELEFONE WHERE numero = ?
            """,
            (numero,)
        )
        return linhas is not None and len(linhas) > 0
    

    def obter_numeros(self) -> list[Numero]:

        pass