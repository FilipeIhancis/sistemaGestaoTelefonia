# MAIN



from ui.Tela import Tela
from database.GerenciadorBanco import GerenciadorBanco
from datetime import datetime
from models import *

diretorio_database = 'database/exemplo.db'



def padrao():
    # Inicia a interface gráfica
    tela = Tela()
    tela.iniciar()


def testar_db():

    banco = GerenciadorBanco(diretorio_database)

    cliente1 = Cliente('Filipe Ihancis', '70072806680', 'filipe@gmail.com', '12345', datetime.now(), [])

    admin1 = Usuario(nome = 'Gabriel',
                     cpf = '57013082198',
                     email = 'gabriel@gmail.com',
                     senha = '12345',
                     data_registro = datetime.now(),
                     tipo = 'ADMINISTRADOR')

    banco.usuarios.salvar(cliente1)
    banco.usuarios.salvar(admin1)

    numero1 = Numero('31999999999', cliente1.cpf, 50.0, None, [], [])
    banco.numeros.salvar(numero1)


    plano1 = Plano(nome = 'Plano 1',
                   dados_mb = 1000,
                   preco = 15.00,
                   maximo_mensagens = 150,
                   maximo_ligacao = 5,
                   minutos_max_ligacao = 5,
                   pacote_mensagem_unitario = 0.1,
                   pacote_minutos_unitario = 0.2)
    
    plano2 = Plano(nome = 'Plano 2',
                   dados_mb = 2000,
                   preco = 20.00,
                   maximo_mensagens = 150,
                   maximo_ligacao = 10,
                   minutos_max_ligacao = 6,
                   pacote_mensagem_unitario = 0.15,
                   pacote_minutos_unitario = 0.2)
    
    plano3 = Plano(nome = 'Plano 3',
                   dados_mb = 3000,
                   preco = 25.00,
                   maximo_mensagens = 200,
                   maximo_ligacao = 15,
                   minutos_max_ligacao = 8,
                   pacote_mensagem_unitario = 0.25,
                   pacote_minutos_unitario = 0.35)
    
    banco.planos.salvar(plano1)
    banco.planos.salvar(plano2)
    banco.planos.salvar(plano3)

    assinatura1 = Assinatura(plano2, datetime.now(), True)
    id_assinatura1 = banco.assinaturas.salvar(assinatura1)
    banco.assinaturas.atribuir_assinatura(id_assinatura1, numero1.numero)


def adicionar_coluna():

    banco = GerenciadorBanco(diretorio_database)

    banco.usuarios.mod()


if __name__ == "__main__":

    #padrao()
    #testar_db()
    adicionar_coluna()