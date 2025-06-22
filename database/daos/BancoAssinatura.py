from database.BancoDeDados import BancoDeDados, T
from models import *
from datetime import datetime

from database.daos.BancoPlano import BancoPlano

class BancoAssinatura(BancoDeDados[Usuario]):

    def __init__(self, diretorio : str = ''):
        super().__init__(diretorio)


    def salvar(self, assinatura : Assinatura) -> int | None:

        id_plano = BancoPlano(self.diretorio).obter_id_plano(assinatura.plano)

        return self.executar(
            """
            INSERT INTO ASSINATURAS (id_plano, data_assinatura, ativa)
            VALUES (?, ?, ?)
            """,
            (
                id_plano,
                assinatura.data_assinatura.isoformat(),
                str(assinatura.ativa)
            )
        )


    def atribuir_assinatura(self, id_assinatura : int, numero : str) -> None:

        # 1. Verificar se o número existe e se já tem assinatura
        resultado = self.executar_select(
            """
            SELECT id_assinatura FROM NUMEROS_TELEFONE WHERE numero = ?
            """,
            (numero,)
        )

        if resultado is None:
            print(f"Erro: Número {numero} não encontrado.")
            return

        if resultado and resultado[0][0] is not None:
            id_assinatura_antiga = resultado[0][0]
            print(f"Removendo assinatura antiga ID: {id_assinatura_antiga}")

            # 2. Excluir a assinatura antiga
            self.executar(
                """
                DELETE FROM ASSINATURAS WHERE id = ?
                """,
                (id_assinatura_antiga,)
            )

        # 3. Fazer o UPDATE no número
        print(f"Atribuindo nova assinatura ID {id_assinatura} ao número {numero}")
        self.executar(
            """
            UPDATE NUMEROS_TELEFONE
            SET id_assinatura = ?
            WHERE numero = ?
            """,
            (id_assinatura, numero)
        )