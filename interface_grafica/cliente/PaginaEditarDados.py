import flet as ft
from interface_grafica.base.SubTela import SubTela


class PaginaEditarDados(SubTela):


    def __init__(self, tela_admin):
        super().__init__(tela_admin=tela_admin)


    def pagina_editar_dados(self) -> None:

        cabecalho = ft.Container(content=ft.Row([
            ft.Column([ft.Text("Editar Dados", size=22, weight=ft.FontWeight.BOLD),
                       ft.Text("CPF: XXX.XXX.XXX-XX")],
                       spacing = 10, expand = True, alignment=ft.alignment.top_left),
            ft.Column([ft.Row([ 
                self.tela.criar_botao('Anexar foto', cor=False),
                ft.Icon(ft.Icons.ACCOUNT_BOX, size = 60) ],
                spacing = 6)],
                alignment=ft.alignment.top_right)
        ]))

        campo = ft.Container( border=ft.border.all(1), border_radius=6, padding=10, expand=True, content=ft.Row([
            # Coluna da esquerda (Email / Senha)
            ft.Column(expand=True, controls=[
                    ft.Row([
                            ft.Column([ ft.Text("EMAIL", weight=ft.FontWeight.BOLD), ft.Text("SENHA", weight=ft.FontWeight.BOLD),],
                                alignment=ft.alignment.top_left),
                            ft.Column([ft.Text("emailqualquer@gmail.com"),ft.Text("*********"),], alignment=ft.alignment.top_right,),
                        ],spacing=30,)]),
            # Coluna da direita (Botões)
            ft.Column(alignment=ft.alignment.top_right, horizontal_alignment=ft.CrossAxisAlignment.END, controls = 
                      [self.tela.criar_botao("Alterar email", funcao = self.editar_email),
                        self.tela.criar_botao("Alterar senha", funcao = self.editar_senha)]),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=50,))

        self.tela.atualizar_pagina(ft.Column([cabecalho, ft.Divider(thickness=2), campo], scroll=ft.ScrollMode.AUTO))


    def modificar_dados(self, e : ft.ControlEvent = None, dialogo : ft.AlertDialog = None) -> None:
        self.tela.page.close(dialogo)
        self.tela.page.update()
        print("Irá modificar os dados")


    def editar_email(self, e : ft.ControlEvent = None) -> None:

        dialogo = None

        novo_email = self.tela.textField(tamanho=200)
        senha = self.tela.textField(tamanho=200)
        senha.password = True

        confirmar = ft.TextButton("Confirmar", on_click = lambda e: self.modificar_dados(e, dialogo))

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
                width=450, height=140, padding = 10, content= 
                ft.Column(spacing = 8, controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                           controls=[ft.Text("Email atual", weight=ft.FontWeight.BOLD), ft.Text("emailqualquer@gmail.com")]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                           controls=[ft.Text("Novo email", weight=ft.FontWeight.BOLD), novo_email]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                           controls=[ft.Text("Digite sua senha", weight=ft.FontWeight.BOLD), senha])
                ])
            ),
            actions=[confirmar, ft.TextButton("Cancelar", on_click=fechar_dialogo)],
            actions_alignment = ft.MainAxisAlignment.END,
            bgcolor=self.tela.cor_dialogo
        )
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

        confirmar = ft.TextButton("Confirmar", on_click= lambda e: self.modificar_dados(e,dialogo))
        confirmar.disabled = True

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
                width=450, height=140, padding=10, content=
                ft.Column(spacing=8, controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Text("Nova senha", weight=ft.FontWeight.BOLD), nova_senha
                    ]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Text("Senha atual", weight=ft.FontWeight.BOLD), senha_atual
                    ]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Text("CPF", weight=ft.FontWeight.BOLD), cpf
                    ])
                ])
            ),
            actions=[confirmar, ft.TextButton("Cancelar", on_click=fechar_dialogo)],
            bgcolor=self.tela.cor_dialogo
        )

        nova_senha.on_change = verificar_campos
        senha_atual.on_change = verificar_campos
        cpf.on_change = verificar_campos

        self.tela.page.dialog = dialogo
        self.tela.page.open(dialogo)
        self.tela.page.update()
        


    """"
    def detalhes_plano(self, e = None):

        info_plano = None 

        def linha(texto1 : str = '', texto2: str = '') -> ft.Row:
            return ft.Row(
                [ft.Text(texto1, weight=ft.FontWeight.BOLD), ft.Text(texto2)],
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            )

        def fechar_info_plano(e = None):
            nonlocal info_plano
            self.tela.page.close(info_plano)
            self.tela.page.update()

        info_plano = ft.AlertDialog(
            modal = True, title = ft.Text("Plano X", weight=ft.FontWeight.BOLD),
            content=ft.Container(width=350, height=160, padding = 10, content = ft.Column([
                linha('Valor', 'R$ ' + '59,90'),
                linha('Dados de Internet', '1000' + ' MB'),
                linha('Valor de recarga', 'R$ ' + '5,20'),
                linha('Máximo de Ligações', '120'),
                linha('Máximo de Mensagens', '150')
            ])),
            actions = [
                ft.TextButton("Sair", on_click = fechar_info_plano)
            ],
            actions_alignment = ft.MainAxisAlignment.END,
        )
        self.tela.page.dialog = info_plano
        self.tela.page.open(info_plano)
        self.tela.page.update()
        """