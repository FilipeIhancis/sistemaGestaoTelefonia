# MAIN
'''


from ui.Tela import Tela

if __name__ == "__main__":
    
    # Inicia a interface gráfica
    tela = Tela()
    tela.iniciar()

    '''


# TESTANDO BANCO DE DADOS

from database.BancoDeDados import BancoDeDados
from datetime import datetime
from models import *

diretorio_database = 'database/exemplo.db'

if __name__ == "__main__":

    cliente1 = Cliente('Filipe Ihancis', '70072806680', 'filipe@gmail.com', '12345', datetime.now(), [])
    numero1 = Numero('31999999999', cliente1.cpf, 50.0, None, [], [])

    banco = BancoDeDados(diretorio_database)
    #banco.criar_tabelas()
    banco.salvar_numero(cliente1, numero1)