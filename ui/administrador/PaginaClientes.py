import flet as ft
from ui.base.SubTela import SubTela

clientes_fake = [
    {"email": "filipe@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666", "5555555555"]},
    {"email": "gaskdjasd@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "akkaka@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "matheus@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "gabriel@gmail.com", "numeros": ["9999999999", "8888888888"]},
]

class PaginaClientes(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)
        

    def criar_cartao_cliente(self, cliente):
        return ft.Container(
            bgcolor = self.tela.cor_cartao_3, alignment= ft.alignment.top_left, border_radius = 5, padding = 10, border=ft.border.all(1), width=280,
            content=ft.Column([
                # Topo com ícone e email
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Row([ft.Icon(ft.Icons.PERSON, size=30), ft.Text(cliente["email"], weight=ft.FontWeight.BOLD)]),
                    ft.IconButton(icon=ft.Icons.SETTINGS, on_click=self.editar_dados_cliente)
                ]),
                ft.Divider(),
                # Área de números com botão editar
                ft.Container( bgcolor = self.tela.cor_cartao_1, border_radius = 10, padding = 10,
                    content = ft.Column([
                        ft.Text("Números", weight=ft.FontWeight.BOLD),
                            *[
                                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                                        ft.Text(numero, expand=True),
                                        self.tela.criar_botao('Editar', cor=False, funcao=self.pagina_edicao_numero)])
                                for numero in cliente["numeros"]
                            ]
                    ])
                ),
                ft.Container( alignment=ft.alignment.center,  padding=10,
                    content= ft.Row([self.tela.criar_botao('Ver faturas', funcao=self.tela.faturas.ver_faturas_cliente),
                                    self.tela.criar_botao('Adicionar número', funcao=self.tela.cadastros.cadastrar_numero)],
                                    spacing = 10, alignment=ft.alignment.center)
                )], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
    

    def pagina_clientes(self) -> None:

        cabecalho = ft.Container(content=ft.Column([
            ft.Row(  [ ft.Row([ft.Icon(ft.Icons.PHONE),ft.Text("Clientes cadastrados", size = 22, weight = ft.FontWeight.BOLD)]),
                       ft.Row([self.tela.criar_botao("Cadastrar cliente", icone=ft.Icons.ADD, funcao=self.tela.cadastros.cadastrar_cliente)])], spacing = 15, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]))

        self.tela.atualizar_pagina(
            ft.Column( controls = [ cabecalho, ft.Divider(thickness=2),
                ft.Row( wrap=True, spacing=20, run_spacing=20, expand = True, scroll = ft.ScrollMode.AUTO,
                        controls=[self.criar_cartao_cliente(c) for c in clientes_fake])
                ], scroll = ft.ScrollMode.AUTO
            )
        )


    def pagina_edicao_numero(self, e) -> None:
        
        cliente = "Joao da Silva".upper()
        cpf_cliente = "XXX.XXX.XXX-XX"

        cabecalho = ft.Container(content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.PHONE),ft.Text("Edição de Número: (31) XXXXX-XXXX", size = 22, weight = ft.FontWeight.BOLD)], spacing = 15),
            ft.Row([ft.Icon(ft.Icons.ACCOUNT_CIRCLE), ft.Text(f"Cliente: {cliente} - CPF: {cpf_cliente}", size = 14)], spacing=15)
        ]))

        def on_change_novo_proprieatario(e = None):
            if novo_proprieatorio.value:
                novo_proprieatorio.label = ''
                novo_proprieatorio.update()

        def on_change_novo_plano(e = None):
            if novo_plano.value:
                novo_plano.label=''
                novo_plano.update()

        cpfs = ['XXX.XXX.XXX-XX', 'YYY.YYY.YYY-YY', 'ZZZ.ZZZ.ZZZ-ZZ']
        planos = ['PLANO 1', 'PLANO 2', 'PLANO 3']

        novo_proprieatorio = self.tela.dropdown(tamanho=220, listaOpcoes=cpfs)
        novo_proprieatorio.on_change = on_change_novo_proprieatario
        novo_proprieatorio.label = "CPF"
        novo_plano = self.tela.dropdown(tamanho=220, listaOpcoes=planos)
        novo_plano.on_change = on_change_novo_plano
        novo_plano.label = "PLANO"

        
        campo2 = ft.Container( height=250,border = ft.border.all(1), border_radius = 6, padding = 20, expand=True,
            content=ft.Column([
            ft.Row( [ft.Icon(ft.Icons.MANAGE_ACCOUNTS), ft.Text("Gerenciamento do Número", weight=ft.FontWeight.BOLD, size=16)],spacing=10),
            ft.Divider(thickness=2),
            ft.Column(controls=[    
                ft.Row([ft.Text("Trocar Proprietário:"), novo_proprieatorio], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("Trocar Plano:"), novo_plano], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            # Linha dos dois botões no final
            ft.Row(controls=[
                    self.tela.criar_botao('Suspender número', cor=False,
                                     funcao = lambda e: self.tela.confirmar(aviso="O número será suspenso após análise.", ao_confirmar=self.suspender_numero)),
                    self.tela.criar_botao('Cancelar número', cor=False,
                                     funcao= lambda e : self.tela.confirmar_identidade(titulo='Cancelar número', ao_confirmar=self.cancelar_numero))
                ], alignment=ft.alignment.top_left, spacing=6)
        ]))

        def linha(texto1:str='', texto2:str='') -> ft.Row:
            return ft.Row(
                controls=[ft.Text(texto1, weight=ft.FontWeight.BOLD), ft.Text(texto2)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )

        campo1 = ft.Container(height=250, expand=True, border = ft.border.all(1), border_radius = 6, padding = 20, content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.INFO), ft.Text("Informações Gerais", weight=ft.FontWeight.BOLD, size=16)],spacing=10),
            ft.Divider(thickness=2),
            ft.Column(spacing = 15, controls=[
                        linha('Número', '(31) XXXXX-XXXX'),
                        linha('Proprietário', 'XXX.XXX.XXX-XX'),
                        linha('Plano Associado', 'Plano X'),
                        linha('Status', 'Ativo')
                    ])
        ]))
        # Botões abaixo
        salvar = self.tela.criar_botao("Salvar")
        cancelar = self.tela.criar_botao("Cancelar", funcao=self.pagina_edicao_numero)

        self.tela.atualizar_pagina(
            ft.Column(scroll = ft.ScrollMode.AUTO, controls=[
                cabecalho, ft.Divider(thickness=2), ft.Column([ft.Row([campo1, campo2]), ft.Row([salvar, cancelar])], spacing=25)]
            )
        )


    def suspender_numero(self, e:ft.ControlEvent = None) -> None:
        
        print("Irá suspender o número")


    def cancelar_numero(self, e:ft.ControlEvent = None) -> None:

        print("Irá cancelar o número")

    
    def editar_dados_cliente(self, e : ft.ControlEvent = None) -> None:

        dialogo = None
        novo_email_usuario = self.tela.textField(tamanho=130, texto=True)
        nova_senha_usuario = self.tela.textField(tamanho=130, texto=True)

        confirmar = ft.TextButton("Confirmar", disabled=True)
        mensagem_erro = ft.Text('Senha incorreta! Tente novamente.', color=ft.Colors.RED, visible=False)

        def linha(conteudo1, conteudo2) -> ft.Row:
            return ft.Row([conteudo1, conteudo2], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        def verificar_campos(e = None):
            nonlocal confirmar
            confirmar.disabled = not (novo_email_usuario.value or nova_senha_usuario.value)
            self.tela.page.update()

        def fechar_dialogo(e=None):
            nonlocal dialogo
            self.tela.page.close(dialogo)
            self.tela.page.update()

        def confirmar_acao(e=None):
            # lógica para confirmar a senha mesmo (IF ->>> cancelar_acao)
            fechar_dialogo()

        def cancelar_acao(e=None):
            fechar_dialogo()

        nova_senha_usuario.on_change = verificar_campos
        novo_email_usuario.on_change = verificar_campos

        # Define o que o botão "Solicitar" vai fazer
        confirmar.on_click = confirmar_acao

        # Cria a caixa de diálogo padrão
        dialogo = ft.AlertDialog(
            modal=True, bgcolor=self.tela.cor_dialogo,
            title=ft.Row([ft.Icon(ft.Icons.MANAGE_ACCOUNTS), ft.Text('Editar dados do cliente', weight=ft.FontWeight.BOLD)], spacing=5),
            content=ft.Container(width=550, height=320, padding=20,
                content= ft.Column([
                    ft.Text("Deixe o campo em branco se não quiser alterar."),
                    ft.Container(padding=ft.padding.all(20), border=ft.border.all(1), border_radius=6, content=ft.Column([
                        linha(ft.Row([ft.Icon(ft.Icons.PERSON), ft.Text("Cliente (CPF)")]), ft.Text("XXX.XXX.XXX-XX")),
                        linha(ft.Text("Email atual"), ft.Text("emailqualquer@gmail.com")),
                        linha(ft.Text("Senha atual"), ft.Text("senhaRandom"))
                    ])),
                    linha(ft.Text("Novo email do usuário", weight=ft.FontWeight.BOLD), novo_email_usuario),
                    linha(ft.Text("Nova senha do usuário", weight=ft.FontWeight.BOLD), nova_senha_usuario)
                ], spacing=15)
            ),
            actions=[confirmar, ft.TextButton("Cancelar", on_click=cancelar_acao)]
        )
        self.tela.page.dialog = dialogo
        self.tela.page.open(dialogo)
        self.tela.page.update()