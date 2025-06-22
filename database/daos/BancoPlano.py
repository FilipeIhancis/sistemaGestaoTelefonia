from database.BancoDeDados import BancoDeDados, T
from models import *
import sqlite3

class BancoPlano(BancoDeDados[Usuario]):

    def __init__(self, diretorio : str = ''):
        super().__init__(diretorio)

    
    def salvar(self, plano : Plano) -> int | None:

        if self.plano_existe(plano.nome):
            print(f"Plano '{plano.nome}' já existe no banco de dados")
            return

        return self.executar(
            """
            INSERT INTO PLANOS (
                nome, dados_mb, preco, maximo_mensagens, maximo_ligacao, minutos_max_ligacao,
                pacote_mensagem_unitario, pacote_minutos_unitario
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (plano.nome, plano.dados_mb, plano.preco, plano.maximo_mensagens, plano.maximo_ligacao, 
            plano.minutos_max_ligacao, plano.pacote_mensagem_unitario, plano.pacote_minutos_unitario)
        )
    

    def plano_existe(self, nome_plano : str) -> bool :

        resultado = self.executar_select(
            """
                SELECT 1 FROM PLANOS WHERE nome = ?
            """,
            (nome_plano,)
        )
        return resultado is not None and len(resultado) > 0


    def obter_plano(self, nome_plano : str = '') -> Plano:

        linhas = self.executar_select(
            """
            SELECT nome, dados_mb, preco, maximo_mensagens, maximo_ligacao, minutos_max_ligacao,
                   pacote_mensagem_unitario, pacote_minutos_unitario
            FROM PLANOS
            WHERE nome = ?
            """,
            (nome_plano,)
        )
        if linhas and len(linhas) > 0:
            linha = linhas[0]
            return Plano(
                nome=linha[0], dados_mb=linha[1], preco=linha[2], maximo_mensagens=linha[3], maximo_ligacao=linha[4], 
                minutos_max_ligacao=linha[5], pacote_mensagem_unitario=linha[6], pacote_minutos_unitario=linha[7]
            )
        else:
            return None
    

    def obter_planos(self) -> list[Plano]:

        linhas = self.executar_select(
            """
            SELECT nome, dados_mb, preco, maximo_mensagens, maximo_ligacao, minutos_max_ligacao,
                   pacote_mensagem_unitario, pacote_minutos_unitario
            FROM PLANOS
            """
        )

        planos: list[Plano] = []

        for linha in linhas:
            plano = Plano(
                nome=linha[0], dados_mb=linha[1], preco=linha[2], maximo_mensagens=linha[3], maximo_ligacao=linha[4],
                minutos_max_ligacao=linha[5], pacote_mensagem_unitario=linha[6], pacote_minutos_unitario=linha[7]
            )
            planos.append(plano)

        return planos


    def obter_id_plano(self, plano : Plano) -> int:

        linhas = self.executar_select(
            """
            SELECT id FROM PLANOS WHERE nome = ?
            """,
            (plano.nome,)
        )
        if linhas and len(linhas) > 0:
            return linhas[0][0]             # Retorna o id (primeira coluna da primeira linha)
        else:
            return None                     # Caso o plano não exista no banco
        

    def adicionar_plano(self, plano : Plano) -> int | None:

        if self.plano_existe(plano.nome):
            return None
        try:
            with sqlite3.connect(self.diretorio) as conn:
                cursor = conn.cursor()
                cursor.execute(
                """
                INSERT INTO PLANOS (nome, dados_mb, preco, maximo_mensagens, maximo_ligacao, minutos_max_ligacao, pacote_mensagem_unitario, pacote_minutos_unitario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (plano.nome, plano.dados_mb, plano.preco, plano.maximo_mensagens, plano.maximo_ligacao, plano.minutos_max_ligacao, 
                 plano.pacote_mensagem_unitario, plano.pacote_minutos_unitario,)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao adicionar plano: {e}")
            return None
        

    def excluir_plano(self, nome_plano : str) -> bool:

        # Primeiro, verifica o id do plano pelo nome
        id_plano = self.obter_id_plano(Plano(nome=nome_plano))

        if id_plano is None:
            print("Plano não encontrado.")
            return False

        # Verifica se alguma assinatura está usando esse plano
        from database.daos.BancoAssinatura import BancoAssinatura
        banco_assinatura = BancoAssinatura(self.diretorio)
        assinaturas_atuais = banco_assinatura.obter_assinaturas()

        for assinatura in assinaturas_atuais:
            plano_da_assinatura = banco_assinatura.obter_plano(assinatura)
            if plano_da_assinatura and plano_da_assinatura.nome == nome_plano:
                print("Não é possível excluir: Existem assinaturas usando esse plano.")
                return False

        # Se passou, pode excluir o plano
        self.executar(
            """
            DELETE FROM PLANOS WHERE id = ?
            """,
            (id_plano,)
        )

        print(f"Plano '{nome_plano}' excluído com sucesso.")
        return True