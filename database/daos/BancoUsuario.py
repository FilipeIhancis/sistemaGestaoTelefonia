from database.BancoDeDados import BancoDeDados, T
from typing import List, Optional
from models import *
from datetime import datetime

class BancoUsuario(BancoDeDados[Usuario]):

    def __init__(self, diretorio : str = ''):
        super().__init__(diretorio)


    def salvar(self, usuario : Usuario):

        self.executar(
            """
                INSERT INTO USUARIO (nome, cpf, email, senha, tipo)
                VALUES (?, ?, ?, ?, ?)
            """,
            (usuario.nome, usuario.cpf, usuario.email, usuario.senha, usuario.tipo)
        )
        self.commit()


    def cpf_existe(self, cpf : str) -> bool:
        resultado = self.executar_select(
            """
                SELECT 1 FROM USUARIO WHERE cpf = ?
            """,
            (cpf,)
        )
        return resultado is not None and len(resultado) > 0
    
    
    def email_existe(self, email : str) -> bool:
        resultado = self.executar_select(
            """
                SELECT 1 FROM USUARIO WHERE email = ?
            """,
            (email,)
        )
        return resultado is not None and len(resultado) > 0

    
    def login(self, email : str, senha : str) -> bool:
        
        resultado = self.executar_select(
            """
                SELECT senha FROM USUARIO WHERE email = ?
            """,
            (email,)
        )

        if resultado and resultado[0][0] == senha:
            return True
        else:
            return False
        
    
    def buscar_usuario(self, email : str, senha : str) -> Usuario:
        resultado = self.executar_select(
            """
            SELECT nome, cpf, email, senha, tipo FROM USUARIO
            WHERE email = ? AND senha = ?
            """,
            (email, senha)
        )
        if resultado and len(resultado) > 0:
            linha = resultado[0]
            nome = linha[0]
            cpf = linha[1]
            tipo = linha[4]

            return Usuario(nome=nome, cpf=cpf, email=email, senha=senha, tipo=tipo, data_registro=datetime.now())
        else:
            return None
        

    def alterar_usuario(self, cpf_usuario : str = '', novo_email : str = '', nova_senha : str = '') -> None:

        campos = []
        parametros = []

        if novo_email != '':
            campos.append("email = ?")
            parametros.append(novo_email)

        if nova_senha != '':
            campos.append("senha = ?")
            parametros.append(nova_senha)

        if not campos:  # segurança
            return

        parametros.append(cpf_usuario)

        self.executar(
            f"""
            UPDATE USUARIO
            SET {', '.join(campos)}
            WHERE cpf = ?
            """,
            tuple(parametros)
        )


    def cpf_existe_email(self, cpf : str, email : str) -> bool:
        
        resultado = self.executar_select(
            """
            SELECT 1 FROM USUARIO WHERE cpf = ? AND email = ?
            """,
            (cpf, email)
        )
        return bool(resultado and len(resultado) > 0)