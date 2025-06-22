import flet as ft
from ui.base.SubTela import SubTela


class PaginaEditarDados(SubTela):


    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)


    def pagina_editar_dados(self) -> None:

        cabecalho = ft.Container(content=
            ft.Row([
                ft.Column([
                        ft.Text("Editar Dados", size=22, weight=ft.FontWeight.BOLD),
                        ft.Row([ft.Text("CPF: ", weight=ft.FontWeight.BOLD), ft.Text(self.tela.usuario.cpf)], spacing=5)
                        ],
                spacing = 10, expand = True, alignment=ft.alignment.top_left),
                ft.Column([
                    ft.Row([self.tela.criar_botao('Anexar foto', cor=False),
                            ft.Icon(ft.Icons.ACCOUNT_BOX, size = 60)],
                            spacing = 6)],
                alignment=ft.alignment.top_right)
            ])
        )

        # Senha censurada:
        senha_usuario : str = ''
        for letra in self.tela.usuario.senha:
            senha_usuario += '*'

        campo = ft.Container( border=ft.border.all(1), border_radius=6, padding=10, expand=True, content=ft.Row([
            # Coluna da esquerda (Email / Senha)
            ft.Column(expand=True, controls=[
                    ft.Row([
                            ft.Column([ ft.Text("EMAIL", weight=ft.FontWeight.BOLD),
                                       ft.Text("SENHA", weight=ft.FontWeight.BOLD),],
                                        alignment=ft.alignment.top_left),
                            ft.Column([ft.Text( self.tela.usuario.email ),
                                       ft.Text(senha_usuario)],
                                        alignment=ft.alignment.top_right,),
                        ], spacing=30,)]),

            # Coluna da direita (Botões)
            ft.Column(alignment=ft.alignment.top_right, horizontal_alignment=ft.CrossAxisAlignment.END, controls = 
                      [self.tela.criar_botao("Alterar email", funcao = self.editar_email),
                        self.tela.criar_botao("Alterar senha", funcao = self.editar_senha)]),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=50,))

        self.tela.atualizar_pagina(ft.Column([cabecalho, ft.Divider(thickness=2), campo], scroll=ft.ScrollMode.AUTO))


    def modificar_dados(self, dialogo:ft.AlertDialog=None, novo_email:str='', nova_senha:str='') -> None:
        self.tela.bd.usuarios.alterar_usuario( self.tela.usuario.cpf, novo_email, nova_senha )
        self.tela.page.close(dialogo)
        self.tela.page.update()


    def editar_email(self, e : ft.ControlEvent = None) -> None:

        dialogo = None

        novo_email = self.tela.textField(tamanho=200)
        senha = self.tela.textField(tamanho=200)
        senha.password = True
        confirmar = ft.TextButton("Confirmar")
        mensagem_erro = ft.Text("Senha incorreta! Tente novamente", color=ft.Colors.RED, visible=False)

        def validar(e:ft.ControlEvent=None) -> None:
            nonlocal novo_email
            nonlocal senha
            nonlocal dialogo
            if self.tela.bd.usuarios.login(self.tela.usuario.email, senha.value):
                self.modificar_dados(dialogo, novo_email.value)
                self.tela.usuario.email = novo_email.value
            else:
                mensagem_erro.visible = True
                self.tela.page.update()

        def fechar_dialogo(e : ft.ControlEvent = None) -> None:
            nonlocal dialogo
            self.tela.page.close(dialogo)
            self.tela.page.update()

        def verificar_campos(e:ft.ControlEvent = None) -> None:
            nonlocal novo_email
            nonlocal senha
            nonlocal confirmar
            confirmar.disabled = not (novo_email.value and senha.value)
            self.tela.page.update()
        
        dialogo = ft.AlertDialog(
            modal = True, title = ft.Row([ft.Icon(ft.Icons.EDIT), ft.Text("Alterar Email", weight=ft.FontWeight.BOLD)], spacing=15),
            content = ft.Container(
                width=450, height=160, padding = 15, content= 
                ft.Column(spacing = 15, controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                           controls=[ft.Text("Email atual", weight=ft.FontWeight.BOLD), ft.Text(self.tela.usuario.email)]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                           controls=[ft.Text("Novo email", weight=ft.FontWeight.BOLD), novo_email]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                           controls=[ft.Text("Confirme sua senha", weight=ft.FontWeight.BOLD), senha]),
                    mensagem_erro
                ])
            ),
            actions=[confirmar, ft.TextButton("Cancelar", on_click=fechar_dialogo)],
            actions_alignment = ft.MainAxisAlignment.END,
            bgcolor=self.tela.cor_dialogo
        )
        confirmar.on_click = validar
        confirmar.disabled = True
        novo_email.on_change = verificar_campos
        senha.on_change = verificar_campos
        self.tela.page.dialog = dialogo
        self.tela.page.open(dialogo)
        self.tela.page.update()


    def editar_senha(self, e : ft.ControlEvent = None) -> None:

        dialogo = None

        nova_senha = self.tela.textField(tamanho=200, texto=True)
        nova_senha.password = True
        senha_atual = self.tela.textField(tamanho=200, texto=True)
        senha_atual.password = True
        cpf = self.tela.textField(tamanho=200, texto=True)

        mensagem_erro = ft.Text("Senha incorreta! Tente novamente", color=ft.Colors.RED, visible=False)

        confirmar = ft.TextButton("Confirmar")
        confirmar.disabled = True

        def validar(e:ft.ControlEvent=None) -> None:
            nonlocal nova_senha
            nonlocal senha_atual
            nonlocal cpf
            nonlocal dialogo
            if self.tela.bd.usuarios.login(self.tela.usuario.email, senha_atual.value):
                if self.tela.bd.usuarios.cpf_existe_email(cpf.value, self.tela.usuario.email):
                    self.modificar_dados(dialogo, nova_senha=nova_senha.value)
                    self.tela.usuario.senha = nova_senha.value
                else:
                    mensagem_erro.visible = True
                    self.tela.page.update()
            else:
                mensagem_erro.visible = True
                self.tela.page.update()

        def verificar_campos(e : ft.ControlEvent = None) -> None:
            nonlocal nova_senha
            nonlocal senha_atual
            nonlocal cpf
            nonlocal dialogo
            confirmar.disabled = not (nova_senha.value and senha_atual.value and cpf.value)
            self.tela.page.update()
            
        def fechar_dialogo(e:ft.ControlEvent=None) -> None:
            nonlocal dialogo
            self.tela.page.close(dialogo)
            self.tela.page.update()

        dialogo = ft.AlertDialog(
            modal = True, title = ft.Row([ft.Icon(ft.Icons.EDIT),ft.Text("Alterar Senha", weight=ft.FontWeight.BOLD)], spacing=15),
            content = ft.Container(
                width=450, height=160, padding=10, content=
                ft.Column(spacing=8, controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Text("Nova senha", weight=ft.FontWeight.BOLD), nova_senha
                    ]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Text("Senha atual", weight=ft.FontWeight.BOLD), senha_atual
                    ]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Text("CPF", weight=ft.FontWeight.BOLD), cpf
                    ]),
                    mensagem_erro
                ])
            ),
            actions=[confirmar, ft.TextButton("Cancelar", on_click=fechar_dialogo)],
            bgcolor=self.tela.cor_dialogo
        )

        confirmar.on_click = validar
        nova_senha.on_change = verificar_campos
        senha_atual.on_change = verificar_campos
        cpf.on_change = verificar_campos

        self.tela.page.dialog = dialogo
        self.tela.page.open(dialogo)
        self.tela.page.update()