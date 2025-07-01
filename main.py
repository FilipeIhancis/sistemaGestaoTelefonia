# MAIN

from ui.Tela import Tela
from database.GerenciadorBanco import GerenciadorBanco
from datetime import datetime
from models import *

diretorio_database = 'database/exemplo.db'


if __name__ == "__main__":

    tela = Tela()
    tela.iniciar()