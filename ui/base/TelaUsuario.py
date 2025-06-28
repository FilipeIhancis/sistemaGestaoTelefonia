import flet as ft
from ui.base.TelaBase import TelaBase
from ui.base.PaginaEditarDados import PaginaEditarDados
from models.usuario import Usuario
from abc import ABC, abstractmethod
import threading


class TelaUsuario(TelaBase, ABC):

    def __init__(self, page : ft.Page, login_callback, usuario : Usuario, *args, **kwargs):
        super().__init__( page = page , *args, **kwargs )
        self.login_callback = login_callback
        self.editar_dados = PaginaEditarDados(self)
        self.usuario = usuario

    @property
    def usuario(self) -> Usuario:
        return self._usuario
    
    @usuario.setter
    def usuario(self, novo_usuario : Usuario):
        if not isinstance(novo_usuario, Usuario):
            raise ValueError("objeto usuário inválido")
        self._usuario = novo_usuario

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


    def confirmar_identidade(self, e : ft.ControlEvent = None, titulo : str = 'Confirmar', ao_confirmar : callable = None, ao_cancelar : callable = None):

        dialogo = None
        senha = self.textField(tamanho=130, texto=True)
        confirmar_senha = self.textField(tamanho=130, texto=True)
        senha.password = True
        confirmar_senha.password = True

        confirmar = ft.TextButton("Confirmar", disabled=True)
        mensagem_erro = ft.Text('Senha incorreta! Tente novamente.', color=ft.Colors.RED, visible=False)

        def verificar_campos(e = None):
            nonlocal senha
            nonlocal confirmar_senha
            nonlocal confirmar
            confirmar.disabled = not (senha.value and confirmar_senha.value)
            self.page.update()

        def fechar_dialogo(e=None):
            nonlocal dialogo
            self.page.close(dialogo)
            self.page.update()

        def confirmar_acao(e=None):
            if (self.bd.usuarios.login(self.usuario.email, senha.value) and senha.value == confirmar_senha.value):
                fechar_dialogo()
                if ao_confirmar:
                    ao_confirmar()
            else:
                mensagem_erro.visible = True
                self.page.update()

        def cancelar_acao(e=None):
            fechar_dialogo()
            if ao_cancelar:
                ao_cancelar()

        senha.on_change = verificar_campos
        confirmar_senha.on_change = verificar_campos

        # Define o que o botão "Solicitar" vai fazer
        confirmar.on_click = confirmar_acao

        # Cria a caixa de diálogo padrão
        dialogo = ft.AlertDialog(
            modal=True, title=ft.Text(titulo, weight=ft.FontWeight.BOLD), bgcolor=self.cor_dialogo,
            content=ft.Container(width=400, height=170, padding=20,
                content= ft.Column([
                    ft.Text("Essa ação requer confirmação de identidade."),
                    ft.Row([ft.Text("Senha"), senha], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([ft.Text("Confirme sua senha"), confirmar_senha], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    mensagem_erro
                ], spacing=15)
            ),
            actions=[confirmar, ft.TextButton("Cancelar", on_click=cancelar_acao)]
        )
        self.page.dialog = dialogo
        self.page.open(dialogo)
        self.page.update()