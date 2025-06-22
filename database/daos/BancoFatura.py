from database.BancoDeDados import BancoDeDados, T
from models import *
from datetime import datetime

class BancoFatura(BancoDeDados[Numero]):

    def __init__(self, diretorio : str = ''):
        super().__init__(diretorio)


    def salvar(self, fatura : Fatura) -> int | None:
        return(
            self.executar(
                """
                INSERT INTO FATURAS (
                    id_numero, valor_pacote_minutos, valor_pacote_mensagem, valor_pacote_dados, valor_total, 
                    emissao, status, mes_referencia, data_emissao, data_vencimento
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    fatura.origem,  # suponho que origem seja o id_numero (int ou str)
                    fatura.valor_pacote_minutos,
                    fatura.valor_pacote_mensagem,
                    0.0,  # valor_pacote_dados não está no construtor, setei zero, ajuste se tiver
                    fatura.valor_total,
                    fatura.emissao.isoformat() if fatura.emissao else None,
                    fatura.status,
                    fatura.mes_referencia.isoformat() if fatura.mes_referencia else None,
                    fatura.data_emissao.isoformat() if fatura.data_emissao else None,
                    None  # data_vencimento: se tiver atributo, use, senão None
                )
            )
        )

    def obter_faturas_numero(self, numero : str) -> list[Fatura] | None:
        
        linhas = self.executar_select(
            """
            SELECT 
                id_numero, valor_pacote_minutos, valor_pacote_mensagem, valor_pacote_dados, valor_total, 
                emissao, status, mes_referencia, data_emissao, data_vencimento
            FROM FATURAS WHERE id_numero = ?
            """,
            (numero,)
        )
        if not linhas:
            return None

        faturas = []
        for linha in linhas:
            fatura = Fatura(
                origem=linha[0],
                valor_pacote_minutos=linha[1],
                valor_pacote_mensagem=linha[2],
                valor_total=linha[4],
                emissao=datetime.fromisoformat(linha[5]) if linha[5] else None,
                status=linha[6],
                mes_referencia=datetime.fromisoformat(linha[7]) if linha[7] else None,
                data_emissao=datetime.fromisoformat(linha[8]) if linha[8] else None
            )
            faturas.append(fatura)

        return faturas