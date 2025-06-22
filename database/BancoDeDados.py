# Código teste para banco de dados

import sqlite3
from datetime import datetime
from models import *
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
T = TypeVar('T')


class BancoDeDados(ABC, Generic[T]):

    def __init__(self, diretorio : str = ''):

        if not isinstance(diretorio, str):
            raise ValueError("Diretório inválido")
        self.diretorio = diretorio
        #self.criar_tabelas()

    @property
    def diretorio(self) -> str:
        return self._diretorio

    @diretorio.setter
    def diretorio(self, novo_dir : str) -> None:
        if not isinstance(novo_dir, str):
            raise ValueError
        self._diretorio = novo_dir


    def executar(self, query : str, params : tuple = ()) -> int | None:
        try:
            with sqlite3.connect(self.diretorio) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao executar query: {e}")


    def executar_select(self, query : str, params : tuple = ()) -> list[tuple]:
        try:
            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()
            cursor.execute(query, params)
            resultado = cursor.fetchall()
            conn.close()
            return resultado
        except Exception as e:
            print(f"Erro ao executar select: {e}")
            return None
        
        
    @abstractmethod
    def salvar(self, objeto : T) -> None:
        pass


    def criar_tabelas(self):

        self.executar("""
            CREATE TABLE IF NOT EXISTS USUARIO (
                nome TEXT NOT NULL,
                cpf TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT CHECK(tipo IN ('CLIENTE', 'ADMINISTRADOR')) NOT NULL
            );
        """)
        self.executar("""
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
        self.executar("""
            CREATE TABLE IF NOT EXISTS ASSINATURAS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_plano INTEGER NOT NULL,
                data_assinatura TEXT NOT NULL,
                ativa TEXT CHECK(ativa IN ('True', 'False')),
                FOREIGN KEY(id_plano) REFERENCES PLANOS(id)
            );
        """)
        self.executar("""
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
        self.executar("""
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
        self.executar("""
            CREATE TABLE IF NOT EXISTS SOLICITACOES (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf_cliente TEXT NOT NULL,
                assunto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                status TEXT CHECK(ativa IN ('True', 'False'))
                FOREIGN KEY (cpf_cliente) REFERENCES USUARIO(cpf)
            );
        """)
        self.executar("""
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
        self.executar("""
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