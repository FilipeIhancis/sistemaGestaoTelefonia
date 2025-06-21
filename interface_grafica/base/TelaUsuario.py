import flet as ft
from interface_grafica.base.TelaBase import TelaBase
from interface_grafica.base.PaginaEditarDados import PaginaEditarDados
from abc import ABC, abstractmethod
import threading


class TelaUsuario(TelaBase, ABC):

    def __init__(self, page : ft.Page, login_callback, *args, **kwargs):
        super().__init__( page = page , *args, **kwargs )
        self._login_callback = login_callback
        self._editar_dados = PaginaEditarDados(self)

    @property
    def login_callback(self):
        return self._login_callback
    
    @login_callback.setter
    def login_callback(self, login):
        if not callable(login):
            raise ValueError("Tela de Login inválida: precisa ser função")
        self._login_callback = login

    @property
    def editar_dados(self):
        return self._editar_dados
    
    @editar_dados.setter
    def editar_dados(self, inst):
        if not isinstance(inst, PaginaEditarDados):
            raise ValueError
        self._editar_dados = inst
    
    @abstractmethod
    def pagina_principal(self) -> None:
        pass

    @abstractmethod
    def paginas_menu_lateral(self, e : ft.ControlEvent) -> None:
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
            modal = True, title = ft.Row([ft.Icon(ft.Icons.LOGOUT), ft.Text("Confirme a ação")], spacing=15),
            content = ft.Text("Deseja sair do aplicativo? (Logout)"),
            actions = [
                ft.TextButton("Sair", on_click = confirmar_saida),
                ft.TextButton("Cancelar", on_click = cancelar_saida)
            ],
            actions_alignment = ft.MainAxisAlignment.END,
            bgcolor=self.cor_dialogo
        )
        self.page.dialog = alerta_dialogo
        self.page.open(alerta_dialogo)
        self.page.update()