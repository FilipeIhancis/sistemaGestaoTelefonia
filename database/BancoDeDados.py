# Código teste para banco de dados

import sqlite3
from datetime import datetime

from models import *


class BancoDeDados():

    def __init__(self, caminho : str):

        self.__conn = sqlite3.connect(caminho)
        self.__cursor = self.__conn.cursor()
        self.criar_tabelas()

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, caminho : str):
        if not isinstance(caminho, str):
            raise ValueError("O caminho do banco de dados deve ser uma string.")
        if self.__conn:
            self.__conn.close()
        try:
            self.__conn = sqlite3.connect(caminho)
            self.__cursor = self.__conn.cursor()
        except sqlite3.Error as e:
            raise ValueError(f"Erro ao conectar ao banco de dados: {e}")
        
    @property
    def cursor(self):
        return self.__cursor
    
    @cursor.setter
    def cursor(self, novo_cursor):
        if not isinstance(novo_cursor, sqlite3.Cursor):
            raise ValueError("O cursor deve ser uma instância de sqlite3.Cursor.")
        self.__cursor = novo_cursor


    # Caso o banco não exista, ele cria as tabelas
    def criar_tabelas(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS USUARIO (
                nome TEXT NOT NULL,
                cpf TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT CHECK(tipo IN ('CLIENTE', 'ADMINISTRADOR')) NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS PLANOS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                dados_mb INTEGER,
                preco REAL,
                maximo_mensagens INTEGER,
                maximo_ligacao INTEGER,
                minutos_max_ligacao INTEGER,
                pacote_mensagem_unitario REAL,
                pacote_minutos_unitario REAL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ASSINATURAS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_plano INTEGER NOT NULL,
                data_assinatura TEXT NOT NULL,
                ativa TEXT CHECK(ativa IN ('True', 'False')),
                FOREIGN KEY(id_plano) REFERENCES PLANOS(id)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS NUMEROS_TELEFONE (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT NOT NULL,
                saldo REAL,
                cpf_cliente TEXT,
                id_assinatura INTEGER,
                FOREIGN KEY(cpf_cliente) REFERENCES USUARIO(cpf),
                FOREIGN KEY(id_assinatura) REFERENCES ASSINATURAS(id)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS FATURAS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_numero INTEGER NOT NULL,
                valor_pacote_minutos REAL NOT NULL,
                valor_pacote_mensagem REAL NOT NULL,
                valor_pacote_dados REAL NOT NULL,
                valor_total REAL NOT NULL,
                emissao TEXT NOT NULL,
                status TEXT NOT NULL,
                mes_referencia TEXT NOT NULL,
                data_emissao TEXT NOT NULL,
                data_vencimento TEXT NOT NULL,
                FOREIGN KEY (id_numero) REFERENCES NUMEROS_TELEFONE(id)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS SOLICITACOES (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf_cliente TEXT NOT NULL,
                assunto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                FOREIGN KEY (cpf_cliente) REFERENCES USUARIO(cpf)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS MENSAGENS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origem TEXT NOT NULL,
                destino TEXT NOT NULL,
                data_envio TEXT NOT NULL,
                conteudo TEXT NOT NULL,
                FOREIGN KEY (origem) REFERENCES NUMEROS_TELEFONE(numero),
                FOREIGN KEY (destino) REFERENCES NUMEROS_TELEFONE(numero)       
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS LIGACOES (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origem TEXT NOT NULL,
                destino TEXT NOT NULL,
                data_inicio TEXT NOT NULL,
                data_fim TEXT NOT NULL,
                duracao INTEGER,
                FOREIGN KEY (origem) REFERENCES NUMEROS_TELEFONE(numero),
                FOREIGN KEY (destino) REFERENCES NUMEROS_TELEFONE(numero)
            );
        """)

        self.conn.commit()

    
    def salvar_numero(self, cliente: Cliente, numero : Numero) -> None:

        self.cursor.execute(
            """
                INSERT INTO NUMEROS_TELEFONE (numero, saldo, cpf_cliente, id_assinatura)
                VALUES (?, ?, ?, ?)
            """ ,
            (numero.numero, numero.saldo, cliente.cpf, None)
        )
        self.conn.commit()

'''

    def listar_tabelas(self):
        print(f"\nTABELAS DO BANCO DE DADOS: ")
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = self.cursor.fetchall()
        for tabela in tabelas:
            print(f"- {tabela[0]}")

    def listar_numeros_por_cliente(self):
        print("\nNÚMEROS POR CLIENTE: ")
        self.cursor.execute("""
            SELECT U.nome, U.cpf, N.numero
            FROM USUARIO U
            LEFT JOIN NUMEROS_TELEFONE N ON U.cpf = N.cpf_do_cliente
            ORDER BY U.nome
        """)
        resultados = self.cursor.fetchall()
        clientes = {}
        for nome, cpf, numero in resultados:
            if nome not in clientes:
                clientes[nome] = []
            if numero:
                clientes[nome].append(numero)

        for nome, numeros in clientes.items():
            if numeros:
                print(f"{nome} possui número(s): {', '.join(numeros)}")
            else:
                print(f"{nome} não possui número associado.")

    def listar_numeros_com_assinatura_ativa(self):
        print("\nNÚMEROS ATIVOS:")
        self.cursor.execute("""
            SELECT N.numero, U.nome, A.ativa
            FROM NUMEROS_TELEFONE N
            JOIN USUARIO U ON U.cpf = N.cpf_do_cliente
            JOIN ASSINATURAS A ON A.id_assinatura = N.id_assinatura
            WHERE A.ativa = 'True'
        """)
        resultados = self.cursor.fetchall()

        if resultados:
            for numero, nome, ativa in resultados:
                print(f"Número: {numero} | Cliente: {nome} | Assinatura ativa: {ativa}")
        else:
            print("Nenhum número com assinatura ativa encontrado.")

    def listar_usuarios_clientes(self):
        print("\nUSUÁRIOS CLIENTES:")
        self.cursor.execute("""
            SELECT nome, cpf
            FROM USUARIO U
            WHERE tipo = 'CLIENTE'
        """)
        resultados = self.cursor.fetchall()

        if resultados:
            for nome_cliente, cpf in resultados:
                print(f'{nome_cliente} (CPF: {cpf})')
        else:
            print("Nenhum cliente encontrado.")

    def numero_existe(self, numero: str) -> bool:
        self.cursor.execute("SELECT 1 FROM NUMEROS_TELEFONE WHERE numero = ?", (numero,))
        return self.cursor.fetchone() is not None

    def cpf_existe(self, cpf: str) -> bool:
        self.cursor.execute("SELECT 1 FROM USUARIO WHERE cpf = ?", (cpf,))
        return self.cursor.fetchone() is not None

    def email_existe(self, email: str) -> bool:
        self.cursor.execute("SELECT 1 FROM USUARIO WHERE email = ?", (email,))
        return self.cursor.fetchone() is not None
    

    def alterar_dados_cliente(self, cpf: str, novo_nome=None, novo_email=None, nova_senha=None) -> None:

        if not self.cpf_existe(cpf):
            print("CPF não encontrado.")
            return

        campos = []
        valores = []

        if novo_nome:
            campos.append("nome = ?")
            valores.append(novo_nome)
        if novo_email:
            if self.email_existe(novo_email):
                print("Email já em uso.")
                return
            campos.append("email = ?")
            valores.append(novo_email)
        if nova_senha:
            campos.append("senha = ?")
            valores.append(nova_senha)

        if not campos:
            print("Nada para atualizar.")
            return

        valores.append(cpf)

        sql = f"UPDATE USUARIO SET {', '.join(campos)} WHERE cpf = ?"
        self.cursor.execute(sql, tuple(valores))
        self.conn.commit()
        print("Dados do cliente atualizados com sucesso.")


    def alterar_numero(self, numero : str, novo_cpf = None, nova_id_assinatura = None):

        if not self.numero_existe(numero):
            print("Número não encontrado.")
            return

        campos = []
        valores = []

        if novo_cpf:
            if not self.cpf_existe(novo_cpf):
                print("CPF informado não existe.")
                return
            campos.append("cpf_do_cliente = ?")
            valores.append(novo_cpf)

        if nova_id_assinatura:
            self.cursor.execute("SELECT 1 FROM ASSINATURAS WHERE id_assinatura = ?", (nova_id_assinatura,))
            if self.cursor.fetchone() is None:
                print("ID de assinatura inválido.")
                return
            campos.append("id_assinatura = ?")
            valores.append(nova_id_assinatura)

        if not campos:
            print("Nada para atualizar.")
            return

        valores.append(numero)

        sql = f"UPDATE NUMEROS_TELEFONE SET {', '.join(campos)} WHERE numero = ?"
        self.cursor.execute(sql, tuple(valores))
        self.conn.commit()
        print("Número alterado com sucesso.")


    def adicionar_usuario(self, nome, cpf, email, senha, tipo):
        try:
            self.cursor.execute("""
                INSERT INTO USUARIO (nome, cpf, email, senha, tipo)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, cpf, email, senha, tipo))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Erro ao adicionar usuário: {e}")


    def adicionar_numero(self, numero, cpf_cliente, id_assinatura):
        try:
            self.cursor.execute("""
                INSERT INTO NUMEROS_TELEFONE (numero, cpf_do_cliente, id_assinatura)
                VALUES (?, ?, ?)
            """, (numero, cpf_cliente, id_assinatura))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Erro ao adicionar Número: {e}")


    def adicionar_plano(self, dados_mb, preco, minutos_max_ligacao):
        try:
            self.cursor.execute("""
                INSERT INTO PLANOS (dados_mb, preco, minutos_max_ligacao)
                VALUES (?, ?, ?)
            """, (dados_mb, preco, minutos_max_ligacao))
            self.conn.commit()
            #return self.cursor.lastrowid  # Retorna ID do plano inserido
        except sqlite3.IntegrityError as e:
            print(f"[ERRO PLANO] {e}")


    def adicionar_assinatura(self, plano_id, data_assinatura, ativa):
        try:
            self.cursor.execute("""
                INSERT INTO ASSINATURAS (plano, data_assinatura, ativa)
                VALUES (?, ?, ?)
            """, (plano_id, data_assinatura, ativa))
            self.conn.commit()
            #return self.cursor.lastrowid  # Retorna ID da assinatura inserida
        except sqlite3.IntegrityError as e:
            print(f"[ERRO ASSINATURA] {e}")
'''


'''
def criar_banco_manualmente():

    # CRIA BANCO DE DADOS
    bd = BancoDeDados('exemplo.db')

    # CPFS INSERIDOS MANUALMENTE
    cpf1 = '12345'
    cpf2 = '54321'
    cpf3 = '01230'

    # NUMERO INSERIDO MANUALMENTE
    numero1 = '31999999999'

    # ADICIONANDO PLANOS MANUALMENTE
    bd.adicionar_plano(dados_mb=3000, preco=39.90, minutos_max_ligacao=200)     # ID = 1
    bd.adicionar_plano(dados_mb=5000, preco=59.90, minutos_max_ligacao=700)     # ID = 2
    bd.adicionar_plano(dados_mb=4000, preco=29.90, minutos_max_ligacao=100)     # ID = 3

    # NOME, CPF, EMAIL, SENHA, TIPO
    bd.adicionar_usuario('Filipe', cpf1, 'filipe@gmail.com', '12345abcd', 'CLIENTE')
    bd.adicionar_usuario('Gabriel', cpf2, 'gabriel@gmail.com', '12000xxxx', 'CLIENTE')
    bd.adicionar_usuario('Henrique', cpf3, 'henrique@gmail.com', '12000xxxx', 'ADMINISTRADOR')

    # ADICIONANDO NÚMERO MANUALMENTE
    # OBS: UM NÚMERO, DE IMEDIATO, PRECISA TER ALGUMA ASSINATURA
    bd.adicionar_assinatura(plano_id = 3, data_assinatura = datetime.now().isoformat(), ativa = 'True')     # ID = 1, ASSINATURA DO NUMERO A SEGUIR:
    bd.adicionar_numero(numero = numero1, cpf_do_cliente = cpf1, id_assinatura = 1)


# MAIN #################################################################################################

# criar_banco_manualmente()

bd = BancoDeDados('exemplo.db')
print("\n========== CONSULTAS ==========")
bd.listar_tabelas()
bd.listar_numeros_por_cliente()
bd.listar_numeros_com_assinatura_ativa()
bd.listar_usuarios_clientes()

print(f"\nO email filipe@gmail.com existe? {bd.email_existe('filipe@gmail.com')}")
print(f"O email filipeihancis@gmail.com existe? {bd.email_existe('filipeihancis@gmail.com')}")
'''