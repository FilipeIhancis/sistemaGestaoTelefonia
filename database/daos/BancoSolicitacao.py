from database.BancoDeDados import BancoDeDados, T
from models import *
from datetime import datetime
from database.daos.BancoUsuario import BancoUsuario

class BancoSolicitacao(BancoDeDados[Solicitacao]):

    def __init__(self, diretorio : str = ''):
        super().__init__(diretorio)
        self.banco_usuarios = BancoUsuario(self.diretorio)

    @property
    def banco_usuarios(self) -> BancoUsuario:
        return self.__banco_usuarios
    
    @banco_usuarios.setter
    def banco_usuarios(self, banco : BancoUsuario):
        if not isinstance(banco, BancoUsuario):
            raise ValueError
        self.__banco_usuarios = banco


    def salvar(self, solicitacao : Solicitacao) -> int | None:

        try:
            self.executar(
                """
                INSERT INTO SOLICITACOES (cpf_cliente, assunto, categoria, status, observacoes)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    solicitacao.cliente_solicitante.cpf, solicitacao.assunto,
                    solicitacao.categoria, str(solicitacao.status), solicitacao.observacoes
                )
            )
            resultado = self.executar_select("SELECT last_insert_rowid()")
            if resultado:
                novo_id = resultado[0][0]
                solicitacao.id = novo_id
                return novo_id
            else:
                return None
        except Exception as e:
            print(f"Erro ao salvar solicitação: {e}")
            return None


    def tornar_resolvida(self, solicitacao : Solicitacao) -> None:
        if solicitacao.id is not None:
            self.executar(
                """
                UPDATE SOLICITACOES
                SET status = 'True'
                WHERE id = ?
                """,
                (solicitacao.id,)
            )

    
    def tornar_pendente(self, solicitacao : Solicitacao) -> None:
        if solicitacao.id is not None:
            self.executar(
                """
                UPDATE SOLICITACOES
                SET status = 'False'
                WHERE id = ?
                """,
                (solicitacao.id,)
            )


    def obter_solicitacoes(self) -> list[Solicitacao]:

        lista: list[Solicitacao] = []

        resultado = self.executar_select("""
            SELECT id, cpf_cliente, assunto, categoria, status, observacoes FROM SOLICITACOES
        """)

        if resultado:
            for linha in resultado:
                id, cpf_cliente, assunto, categoria, status_str, observacoes = linha
                status = True if status_str == 'True' else False
                solicitacao = Solicitacao(id = id, 
                                          cliente_solicitante=self.banco_usuarios.buscar_usuario_cpf(cpf=cpf_cliente), 
                                          assunto=assunto, 
                                          categoria=categoria, 
                                          status=status, 
                                          observacoes=observacoes)
                lista.append(solicitacao)

        return lista


    def obter_solicitacoes_cliente(self, usuario : Usuario) -> list[Solicitacao]:

        lista: list[Solicitacao] = []

        resultado = self.executar_select("""
            SELECT id, cpf_cliente, assunto, categoria, status, observacoes FROM SOLICITACOES
            WHERE cpf_cliente = ?
        """, (usuario.cpf,))

        if resultado:
            for linha in resultado:
                id, cpf_cliente, assunto, categoria, status_str, observacoes = linha
                status = True if status_str == 'True' else False
                solicitacao = Solicitacao(id = id, 
                                          cliente_solicitante=self.banco_usuarios.buscar_usuario_cpf(cpf=cpf_cliente), 
                                          assunto=assunto, 
                                          categoria=categoria, 
                                          status=status, 
                                          observacoes=observacoes)
                lista.append(solicitacao)
        return lista
    

    def pendentes(self) -> list[Solicitacao]:
        resultados = self.executar_select(
            """
            SELECT id, cpf_cliente, assunto, categoria, status, observacoes FROM SOLICITACOES
            WHERE status = 'False'
            """
        )
        solicitacoes = []
        if resultados:
            for linha in resultados:
                solicitacao = Solicitacao(id=linha[0],
                    cliente_solicitante= self.banco_usuarios.buscar_usuario_cpf(cpf=linha[1]) , 
                    assunto=linha[2], categoria=linha[3], status=False, observacoes=linha[5]
                )
                solicitacoes.append(solicitacao)

        return solicitacoes

    
    def resolvidas(self) -> list[Solicitacao]:

        resultados = self.executar_select(
            """
            SELECT id, cpf_cliente, assunto, categoria, status, observacoes FROM SOLICITACOES
            WHERE status = 'True'
            """
        )
        solicitacoes = []
        if resultados:
            for linha in resultados:
                solicitacao = Solicitacao(id=linha[0],
                    cliente_solicitante= self.banco_usuarios.buscar_usuario_cpf(cpf=linha[1]) , 
                    assunto=linha[2], categoria=linha[3], status=True, observacoes=linha[5]
                )
                solicitacoes.append(solicitacao)

        return solicitacoes