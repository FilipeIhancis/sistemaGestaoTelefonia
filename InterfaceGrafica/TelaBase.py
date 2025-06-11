import flet as ft
from abc import ABC, abstractmethod
import threading


class TelaBase(ABC):

    def __init__(self, page : ft.Page, login_callback):

        super().__init__()
        self.page = page
        self.login_callback = login_callback
        self.conteudo_pagina_principal = ft.Container(expand=True, alignment=ft.alignment.center)

        # Cores do aplicativo
        self.cor_botao = "#372D6D"
        self.cor_cartao_1 = "#12101B"
        self.cor_cartao_2 = "#272244"
        self.cor_cartao_3 = "#15131D"


    @abstractmethod
    def pagina_principal(self) -> None:
        pass


    def sair(self) -> None:

        alerta_dialogo = None 

        def confirmar_saida(e = None):
            nonlocal alerta_dialogo
            self.page.close(alerta_dialogo)
            self.page.update()
            threading.Timer(0.2, lambda: self.login_callback(self.page)).start()
        
        def cancelar_saida(e = None):
            nonlocal alerta_dialogo
            self.page.close(alerta_dialogo)
            self.page.update()
            threading.Timer(0.2, lambda: self.pagina_principal()).start()

        alerta_dialogo = ft.AlertDialog(
            modal = True, title = ft.Text("Confirme a ação"),
            content = ft.Text("Deseja sair?"),
            actions = [
                ft.TextButton("Sair", on_click = confirmar_saida),
                ft.TextButton("Cancelar", on_click = cancelar_saida)
            ],
            actions_alignment = ft.MainAxisAlignment.END,
        )
        self.page.dialog = alerta_dialogo
        self.page.open(alerta_dialogo)
        self.page.update()


    def definir_cor_vermelho(self) -> None:
        self.cor_botao = "#372D6D"
        self.cor_cartao_1 = "#282727"
        self.cor_cartao_2 = "#272244"

    
    def definir_cor_azul(self) -> None:
        self.cor_botao = "#372D6D"
        self.cor_cartao_1 = "#282727"
        self.cor_cartao_2 = "#272244"