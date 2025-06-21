import flet as ft
from ui.base.SubTela import SubTela

class PaginaCadastro(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)


    def cadastrar_cliente(self, e : ft.ControlEvent = None):

        cabecalho = ft.Text("Cadastro de novo cliente", size=22, weight=ft.FontWeight.BOLD)

        cadastrar = self.tela.criar_botao('Cadastrar')
        cadastrar.disabled = True

        def validar(e=None):
            # Só habilita se ambos os campos estiverem preenchidos
            cadastrar.disabled = not (cpf.value.strip() and email.value.strip())
            self.tela.page.update()

        cpf = ft.TextField(width=200, on_change=validar, border_color=ft.Colors.WHITE, focused_border_color=ft.Colors.WHITE)
        email = ft.TextField(width=200, on_change=validar, border_color=ft.Colors.WHITE, focused_border_color=ft.Colors.WHITE)
        senha = ft.Text("senhaRandom")

        campo = ft.Container( border=ft.border.all(1), border_radius=6, padding=10, expand=True, 
            content=ft.Column([
                    ft.Row(
                        [ft.Text('CPF', weight=ft.FontWeight.BOLD), cpf,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [ft.Text('EMAIL', weight=ft.FontWeight.BOLD), email,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [ft.Text('SENHA', weight=ft.FontWeight.BOLD), senha],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [cadastrar, self.tela.criar_botao('Cancelar')],
                        spacing=10, alignment=ft.MainAxisAlignment.END,
                    )
                ], spacing=15, width=500
            )
        )
        self.tela.atualizar_pagina(ft.Column(controls=[cabecalho, ft.Divider(thickness=2), campo], scroll=ft.ScrollMode.AUTO))


    def cadastrar_plano(self, e) -> None:

        cabecalho = ft.Row([ft.Icon(ft.Icons.LIST_ALT), ft.Text("Novo Plano", size = 22, weight=ft.FontWeight.BOLD)], spacing=10)

        def criar_linha(texto : str, textField : ft.TextField) -> ft.Row:
            return ft.Row(
                [ft.Text(value=texto, weight=ft.FontWeight.BOLD), textField],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )

        nome = self.tela.textField(tamanho=100)
        max_lig = self.tela.textField(tamanho=100, inteiro=True)
        max_msg = self.tela.textField(tamanho=100, inteiro=True)
        dados_internet = self.tela.textField(tamanho=100, inteiro=True)
        valor_mensal = self.tela.textField(tamanho=100, flutuante=True)
        valor_recarga = self.tela.textField(tamanho=100, flutuante=True)
        valor_pacote_msg = self.tela.textField(tamanho=100, flutuante=True)
        valor_pacote_lig = self.tela.textField(tamanho=100, flutuante=True)
        dados_internet.suffix_text = 'MB'
        valor_mensal.prefix_text = 'R$'
        valor_recarga.prefix_text = 'R$'
        valor_pacote_lig.prefix_text = 'R$'
        valor_pacote_msg.prefix_text = 'R$'
        
        dados = ft.Container(padding=15, width=350, expand=True, border=ft.border.all(1), border_radius=8, content= ft.Column([
            ft.Row([ ft.Icon(ft.Icons.INFO), ft.Text('Dados',size=18, weight=ft.FontWeight.BOLD) ], spacing=10),
            ft.Divider(thickness=1),
            criar_linha('Nome', nome),
            criar_linha('Dados de Internet (MB)', dados_internet),
            criar_linha('Máximo de ligações', max_lig),
            criar_linha('Máximo de mensagens', max_msg)
            ])
        )
        valores = ft.Container(padding = 15, width = 400, expand=True, border=ft.border.all(1), border_radius=8, content=ft.Column([
            ft.Row([ ft.Icon(ft.Icons.ATTACH_MONEY), ft.Text('Valores',size=18, weight=ft.FontWeight.BOLD) ], spacing=10),
            ft.Divider(thickness=1),
            criar_linha('Valor mensal', valor_mensal),
            criar_linha('Valor de recarga', valor_recarga),
            criar_linha('Valor pacote de mensagens', valor_pacote_msg),
            criar_linha('Valor pacote de ligações', valor_pacote_lig)
        ]))

        botoes = ft.Row(spacing = 5, controls=[
            self.tela.criar_botao('Criar', funcao=None), self.tela.criar_botao('Cancelar')
        ])

        self.tela.atualizar_pagina(
            ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
            cabecalho, ft.Divider(thickness=2), ft.Row([dados, valores]), botoes
            ])
        )


    def cadastrar_numero(self, e = None) -> None:

        def criar_linha(texto1 : str, texto2 : str) -> ft.Row:
            return ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls= [ft.Text(value=texto1, weight=ft.FontWeight.BOLD), ft.Text(value=texto2)])

        cabecalho = ft.Row([
            ft.Icon(ft.Icons.ADD_IC_CALL), ft.Text("Adicionar número ao sistema", size=22, weight=ft.FontWeight.BOLD)
        ])

        cpfs = ['XXX.XXX.XXX-XX', 'YYY.YYY.YYY-YY', 'ZZZ.ZZZ.ZZZ-ZZ']
        planos = ['PLANO 1', 'PLANO 2', 'PLANO 3']

        proprietario = self.tela.dropdown('Escolha um cliente', cpfs)
        plano = self.tela.dropdown('Escolha um plano', planos)

        configDados = ft.Container( padding = 20, border_radius=8, border=ft.border.all(1), expand=True, content=ft.Column([
                # Cabeçalho do card
                ft.Container(padding = ft.padding.only(bottom=8), content=
                    ft.Row(spacing=5, controls=[ft.Icon(ft.Icons.SETTINGS), ft.Text("Configuração de dados", size=18, weight=ft.FontWeight.BOLD)])
                ),
                # Número + Gerar número aleatório
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("Número", weight=ft.FontWeight.BOLD),
                    ft.Row(spacing=10, controls=[
                        ft.Text("(31) XXXXX-XXXX"), ft.IconButton(icon=ft.Icons.AUTORENEW)
                    ])
                ]),
                # Proprietário + Dropdown
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("Proprietário", weight=ft.FontWeight.BOLD), proprietario
                ]),
                # Plano + Dropdown
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("Plano", weight=ft.FontWeight.BOLD), plano
                ]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("Saldo inicial", weight=ft.FontWeight.BOLD), self.tela.textField(prefixo='R$ ', tamanho=150, flutuante=True)
                ])
            ])
        )

        info = ft.Container( padding = 20, border_radius=8, border=ft.border.all(1), expand=True, content=ft.Column([
                ft.Container(padding = ft.padding.only(bottom=18) , content=
                    ft.Row(spacing=5, controls=[ft.Icon(ft.Icons.INFO), ft.Text("Informações do número", size=18, weight=ft.FontWeight.BOLD)])
                ),
                criar_linha('Número', '(31) XXXXXX-XXXX'), ft.Divider(thickness=1),
                criar_linha('Proprietário', 'XXX.XXX.XXX-XX'), ft.Divider(thickness=1),
                criar_linha('Plano', 'NomePlano'), ft.Divider(thickness=1),
                criar_linha('Dados (MB)', '1000 MB'), ft.Divider(thickness=1),
                criar_linha('Máximo de ligações', '20'), ft.Divider(thickness=1),
                criar_linha('Máximo de mensagens', '10')
            ], spacing=2)
        )

        botoes = ft.Row(spacing=6, controls=[
            self.tela.criar_botao('Criar número'), self.tela.criar_botao('Cancelar')
        ])

        info.height = configDados.height

        self.tela.atualizar_pagina(ft.Column([
            cabecalho, ft.Divider(thickness=2), ft.Row([configDados, info]), botoes])
        )