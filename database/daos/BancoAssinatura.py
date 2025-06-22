from database.BancoDeDados import BancoDeDados, T
from models import *
from datetime import datetime

class BancoAssinatura(BancoDeDados[Usuario]):

    def __init__(self, diretorio : str = ''):
        super().__init__(diretorio)


    def salvar(self, assinatura : Assinatura) -> int | None:
        
        from database.daos.BancoPlano import BancoPlano
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

    
    def obter_assinaturas(self) -> list[Assinatura]:

        assinaturas: list[Assinatura] = []
        resultado = self.executar_select("""
            SELECT id_plano, data_assinatura, ativa FROM ASSINATURAS
        """)

        if resultado:
            for linha in resultado:
                id_plano, data_assinatura_str, ativa_str = linha
                plano = self.obter_plano_via_id(id_plano)
                data_assinatura = datetime.fromisoformat(data_assinatura_str)
                ativa = True if ativa_str == 'True' else False
                assinatura = Assinatura(plano, data_assinatura, ativa)
                assinaturas.append(assinatura)

        return assinaturas


    def obter_assinatura(self, numero: Numero) -> Assinatura:

        resultado = self.executar_select(
            """
            SELECT id_assinatura FROM NUMEROS_TELEFONE WHERE numero = ?
            """,
            (numero.numero,)
        )

        if resultado and resultado[0][0] is not None:
            id_assinatura = resultado[0][0]

            # Agora busca os dados da assinatura
            dados_assinatura = self.executar_select(
                """
                SELECT id_plano, data_assinatura, ativa FROM ASSINATURAS WHERE id = ?
                """,
                (id_assinatura,)
            )

            if dados_assinatura:
                id_plano, data_assinatura_str, ativa_str = dados_assinatura[0]

                # Busca o Plano correspondente
                plano = self.obter_plano_via_id(id_plano)

                assinatura = Assinatura(
                    plano=plano,
                    data_assinatura=datetime.fromisoformat(data_assinatura_str),
                    ativa=(ativa_str == 'True')
                )
                return assinatura

        return None
    
    
    def obter_plano_via_id(self, id_plano: int) -> Plano | None:
        
        resultado = self.executar_select(
            """
            SELECT nome, dados_mb, preco, maximo_mensagens, maximo_ligacao,
                minutos_max_ligacao, pacote_mensagem_unitario, pacote_minutos_unitario
            FROM PLANOS
            WHERE id = ?
            """,
            (id_plano,)
        )
        if resultado:
            linha = resultado[0]
            plano = Plano(
                nome=linha[0],
                dados_mb=linha[1],
                preco=linha[2],
                maximo_mensagens=linha[3],
                maximo_ligacao=linha[4],
                minutos_max_ligacao=linha[5],
                pacote_mensagem_unitario=linha[6],
                pacote_minutos_unitario=linha[7]
            )
            return plano

        return None


    def obter_plano(self, assinatura : Assinatura) -> Plano:

        # Primeiro, buscar o id_plano no banco (caso não tenha certeza se o objeto plano veio completo)
        resultado = self.executar_select(
            """
            SELECT id_plano FROM ASSINATURAS
            WHERE data_assinatura = ? AND ativa = ?
            """,
            (
                assinatura.data_assinatura.isoformat(),
                str(assinatura.ativa)
            )
        )

        if resultado:
            id_plano = resultado[0][0]
            return self.obter_plano_via_id(id_plano)

        return None