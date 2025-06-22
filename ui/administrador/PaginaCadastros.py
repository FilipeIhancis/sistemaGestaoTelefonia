import flet as ft
from ui.base.SubTela import SubTela
from models.usuario import Usuario
from datetime import datetime
from models.plano import Plano

class PaginaCadastro(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)


    def cadastrar_cliente(self, e : ft.ControlEvent = None):

        cpf = self.tela.textField(tamanho=200, inteiro=True)
        nome = self.tela.textField(tamanho=200, texto=True)
        email = self.tela.textField(tamanho=200, texto=True)
        senha = ft.Text("senhaRandom")
        mensagem_erro = ft.Text("Dados inválidos. Verifique se o CPF já possui cadastro no sistema.", color=ft.Colors.RED, visible=False)

        cadastrar = self.tela.criar_botao('Cadastrar')
        cadastrar.disabled = True

        def adicionar(e : ft.ControlEvent = None) -> None:
            try:
                cliente = Usuario(nome.value, cpf.value, email.value, senha.value, datetime.now(), 'CLIENTE')
                if (self.tela.bd.usuarios.adicionar_cliente(usuario = cliente)):
                    mensagem_erro.visible = False
                    self.tela.page.update()
                    self.tela.page.open(
                        ft.AlertDialog(
                            title = ft.Text("Cliente adicionado com sucesso"),
                            alignment=ft.alignment.center,
                            bgcolor = self.tela.cor_dialogo
                        )
                    )
                else:
                    mensagem_erro.visible = True
                    self.tela.page.update()

            except ValueError:
                mensagem_erro.visible = True
                self.tela.page.update()

        def validar(e : ft.ControlEvent = None) -> None:
            cadastrar.disabled = not (cpf.value.strip() and email.value.strip())
            self.tela.page.update()

        cadastrar.on_click = adicionar
        cpf.on_change = validar
        email.on_change = validar
        nome.on_change = validar

        cabecalho = ft.Text("Cadastro de novo cliente", size=22, weight=ft.FontWeight.BOLD)

        campo = ft.Container( border=ft.border.all(1), border_radius=6, padding=ft.padding.all(25), expand=True, 
            content=ft.Column([
                    ft.Row(
                        [ft.Text('CPF CLIENTE', weight=ft.FontWeight.BOLD), cpf,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [ft.Text('NOME CLIENTE', weight=ft.FontWeight.BOLD), nome,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [ft.Text('EMAIL', weight=ft.FontWeight.BOLD), email,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [ft.Text('SENHA (RANDÔMICA)', weight=ft.FontWeight.BOLD), senha],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    mensagem_erro,
                    ft.Row( [cadastrar], spacing=10, alignment=ft.MainAxisAlignment.END )
                ], spacing=15, width=500
            )
        )
        self.tela.atualizar_pagina(ft.Column(controls=[cabecalho, ft.Divider(thickness=2), campo], scroll=ft.ScrollMode.AUTO))


    def cadastrar_plano(self, e : ft.ControlEvent) -> None:

        cabecalho = ft.Row([ft.Icon(ft.Icons.LIST_ALT), ft.Text("Novo Plano", size = 22, weight=ft.FontWeight.BOLD)], spacing=10)

        def criar_linha(texto : str, textField : ft.TextField) -> ft.Row:
            return ft.Row(
                [ft.Text(value=texto, weight=ft.FontWeight.BOLD), textField],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        
        # Entradas do administrador:
        nome = self.tela.textField(tamanho=100)
        max_lig = self.tela.textField(tamanho=100, inteiro=True)
        max_msg = self.tela.textField(tamanho=100, inteiro=True)
        dados_internet = self.tela.textField(tamanho=100, inteiro=True)
        minutos_max = self.tela.textField(tamanho = 100, inteiro=True)
        valor_mensal = self.tela.textField(tamanho=100, flutuante=True)
        valor_pacote_msg = self.tela.textField(tamanho=100, flutuante=True)
        valor_pacote_lig = self.tela.textField(tamanho=100, flutuante=True)

        botao_criar_plano = self.tela.criar_botao('Criar Plano')
        botao_criar_plano.disabled = True

        dados_internet.suffix_text = 'MB'
        valor_mensal.prefix_text = 'R$ '
        valor_pacote_lig.prefix_text = 'R$ '
        valor_pacote_msg.prefix_text = 'R$ '

        def adicionar(e : ft.ControlEvent = None) -> None:
            
            try:
                plano = Plano(nome.value, int(dados_internet.value), float(valor_mensal.value), int(max_msg.value),
                          int(max_lig.value), int(minutos_max.value), float(valor_pacote_msg.value), float(valor_pacote_lig.value))
            except ValueError:
                self.tela.page.open(ft.AlertDialog(
                    title = ft.Text("Erro nos valores", weight=ft.FontWeight.BOLD),
                    content= ft.Text("Preencha os campos corretamente.")
                ))
            if self.tela.bd.planos.plano_existe(nome.value):
                self.tela.page.open(ft.AlertDialog(
                    title = ft.Row([ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED), ft.Text(f"ERRO", weight=ft.FontWeight.BOLD)], spacing=5),
                    content=ft.Text(f"O plano '{nome.value}' já existe no sistema."),
                    bgcolor=self.tela.cor_dialogo
                ))
                self.tela.page.update()
            else:
                self.tela.bd.planos.adicionar_plano(plano)
                self.tela.page.open(ft.AlertDialog(
                    bgcolor=self.tela.cor_dialogo,
                    title=ft.Text('Plano adicionado', weight=ft.FontWeight.BOLD), 
                    content=ft.Text(f"O plano '{nome.value}' foi adicionado ao sistema com sucesso. Acesse a aba 'Planos' para visualizar.")
                ))
                self.tela.page.update()

        def validar(e : ft.ControlEvent = None) -> None:
            botao_criar_plano.disabled = not (nome.value and max_lig.value and max_msg.value and dados_internet.value and minutos_max.value
                                              and valor_mensal.value and valor_pacote_msg.value and valor_pacote_lig.value)
            self.tela.page.update()

        campos = [nome, max_lig, max_msg, dados_internet, minutos_max, dados_internet, minutos_max, valor_mensal, valor_pacote_lig, valor_pacote_msg]
        for campo in campos:
            val_original = campo.on_change
            def combinado(e, original = val_original):
                if original:
                    original(e)
                validar(e)
            campo.on_change = combinado

        botao_criar_plano.on_click = adicionar
        minutos_max.on_change = validar
        nome.on_change = validar
        max_lig.on_change = validar
        max_msg.on_change = validar
        dados_internet.on_change = validar
        valor_mensal.on_change = validar
        valor_pacote_lig.on_change = validar
        valor_pacote_msg.on_change = validar

        dados = ft.Container(padding=15, width=350, expand=True, border=ft.border.all(1), border_radius=8, content= ft.Column([
            ft.Row([ft.Icon(ft.Icons.INFO), ft.Text('Dados',size=18, weight=ft.FontWeight.BOLD) ], spacing=10),
            ft.Divider(thickness=1),
            criar_linha('Nome', nome),
            criar_linha('Dados de Internet (MB)', dados_internet),
            criar_linha('Máximo de ligações', max_lig),
            criar_linha('Minutos máx. em ligação', minutos_max),
            criar_linha('Máximo de mensagens', max_msg)
            ])
        )
        valores = ft.Container(padding = 15, width = 400, expand=True, border=ft.border.all(1), border_radius=8, content=ft.Column([
            ft.Row([ ft.Icon(ft.Icons.ATTACH_MONEY), ft.Text('Valores',size=18, weight=ft.FontWeight.BOLD) ], spacing=10),
            ft.Divider(thickness=1),
            criar_linha('Valor mensal', valor_mensal),
            criar_linha('Valor pacote de mensagens', valor_pacote_msg),
            criar_linha('Valor pacote de ligações', valor_pacote_lig)
        ]))

        self.tela.atualizar_pagina(
            ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
            cabecalho, ft.Divider(thickness=2), ft.Row([dados, valores]), botao_criar_plano
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