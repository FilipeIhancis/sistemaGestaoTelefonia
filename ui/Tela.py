import flet as ft
from ui.base.TelaBase import TelaBase
from ui.cliente.TelaCliente import TelaCliente
from ui.administrador.TelaAdministrador import TelaAdministrador

# Credenciais cadastradas (simulação)
email_cadastrado = ["filipe@gmail.com", "admin@gmail.com", "admin"]
senha_cadastrada = "12345"


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
        self.page.window_width = 800
        self.page.window_height = 800
        self.page.window_resizable = True

        # Campos de entrada
        email = ft.TextField(label='Email', text_align=ft.TextAlign.LEFT, width=200, border_color=ft.Colors.WHITE, focused_border_color=ft.Colors.WHITE)
        senha = ft.TextField(label='Senha', text_align=ft.TextAlign.LEFT, width=200, password = True, border_color=ft.Colors.WHITE, focused_border_color=ft.Colors.WHITE)
        botao_entrar = ft.ElevatedButton(text='Entrar', width=200, disabled = True)

        # Textos na tela
        mensagem_login = ft.Text(value='Login', size=20)
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

        # Eventos: verifica se os campos foram preenchidas para deixar o botão clicável/visível
        # Ao clicar no botão (on_click), vai para a função entrar()
        email.on_change = validar
        senha.on_change = validar
        botao_entrar.on_click = logar

        # Layout final (formatação da tela)
        self.page.add(
            ft.Row(controls=[
                    ft.Column(
                        controls=[mensagem_login, email, senha, botao_entrar, mensagem_erro],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )],
                alignment=ft.MainAxisAlignment.CENTER )
        )


    def validar_credenciais(self, e = None, email : str = '', senha : str = '') -> bool:
        return self.bd.usuarios.login(email, senha)