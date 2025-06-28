import flet as ft
from ui.base.TelaBase import TelaBase
from ui.cliente.TelaCliente import TelaCliente
from ui.administrador.TelaAdministrador import TelaAdministrador


class Tela(TelaBase):

    def __init__(self):
        super().__init__(None)

    def iniciar(self):
        super().iniciar(self.pagina_login)


    def pagina_login(self, page: ft.Page) -> None:

        self.page = page
        self.page.clean()
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 1200
        self.page.window_height = 1000
        self.page.window_resizable = True

        # Campos de entrada
        email = ft.TextField(label='Email', text_align=ft.TextAlign.LEFT, width=200, border_color=ft.Colors.WHITE, focused_border_color=ft.Colors.WHITE)
        senha = ft.TextField(label='Senha', text_align=ft.TextAlign.LEFT, width=200, password = True, can_reveal_password = True, 
                             border_color=ft.Colors.WHITE, focused_border_color=ft.Colors.WHITE)
        botao_entrar = self.criar_botao("Entrar")
        botao_entrar.disabled = True
        # botao_entrar = ft.ElevatedButton(text='Entrar', width=200, disabled = True)

        # Textos na tela
        mensagem_login = ft.Text(value='Login', size=20, weight=ft.FontWeight.BOLD)
        mensagem_erro = ft.Text(
            value='Usuário ou senha inválidos.',
            color=ft.Colors.RED,  # Corrigido: ft.Colors -> ft.colors
            visible=False, size=12
        )

        # Validação dos campos
        def validar(e = None):
            botao_entrar.disabled = not (email.value and senha.value)
            mensagem_erro.visible = False  # Esconde erro ao digitar
            self.page.update()

        def logar(e = None):

            if (self.validar_credenciais(email = email.value, senha = senha.value)):

                usuario = self.bd.usuarios.buscar_usuario(email.value, senha.value)

                if usuario.tipo == 'CLIENTE':
                    tela_cliente = TelaCliente(self.page, self.pagina_login, usuario)
                    tela_cliente.pagina_principal()
                elif usuario.tipo == 'ADMINISTRADOR':
                    tela_adm = TelaAdministrador(self.page, self.pagina_login, usuario)
                    tela_adm.pagina_principal()
                else:
                    raise ValueError("Tipo inválido")
            else:
                mensagem_erro.visible = True
                self.page.update()

        email.on_change = validar
        senha.on_change = validar
        botao_entrar.on_click = logar
        
        self.page.add(
            ft.Row(controls=[
                ft.Container(padding=ft.padding.all(35), border=ft.border.all(1, ft.Colors.WHITE), border_radius=10, bgcolor=self.cor_dialogo, content=
                            ft.Column(
                                controls=[ft.Container(content=mensagem_login, padding=ft.padding.only(bottom=20)),
                                        email, senha, botao_entrar, mensagem_erro ],
                                alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15
                            )
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER )
        )


    def validar_credenciais(self, e = None, email : str = '', senha : str = '') -> bool:
        return self.bd.usuarios.login(email, senha)