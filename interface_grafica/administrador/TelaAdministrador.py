import flet as ft
from interface_grafica.base.TelaUsuario import TelaUsuario

from interface_grafica.administrador.PaginaSolicitacoes import PaginaSolicitacoes
from interface_grafica.administrador.PaginaCadastros import PaginaCadastro
from interface_grafica.administrador.PaginaPlanos import PaginaPlanos
from interface_grafica.administrador.PaginaFaturas import PaginaFaturas

clientes = [
    {"email": "filipe@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666", "5555555555"]},
    {"email": "gaskdjasd@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "akkaka@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "matheus@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "gabriel@gmail.com", "numeros": ["9999999999", "8888888888"]},
]


class TelaAdministrador(TelaUsuario):

    def __init__(self, page : ft.Page, login_callback):
        super().__init__(page = page, login_callback = login_callback)

        self.__solicitacoes = PaginaSolicitacoes(self)
        self.__cadastros = PaginaCadastro(self)
        self.__planos = PaginaPlanos(self)
        self.__faturas = PaginaFaturas(self)

    @property
    def solicitacoes(self):
        return self.__solicitacoes
    
    @solicitacoes.setter
    def solicitacoes(self, inst : PaginaSolicitacoes):
        if not isinstance(inst, PaginaSolicitacoes):
            raise ValueError("")
        self.__solicitacoes = inst
    
    @property
    def cadastros(self):
        return self.__cadastros
    
    @cadastros.setter
    def cadastros(self, inst : PaginaCadastro):
        if not isinstance(inst, PaginaCadastro):
            raise ValueError("")
        self.__cadastros = inst

    @property
    def planos(self):
        return self.__planos
    
    @planos.setter
    def planos(self, inst : PaginaPlanos):
        if not isinstance(inst, PaginaPlanos):
            raise ValueError("")
        self.__planos = inst

    @property
    def faturas(self):
        return self.__faturas
    
    @faturas.setter
    def faturas(self, inst : PaginaFaturas):
        if not isinstance(inst, PaginaFaturas):
            raise ValueError("")
        self.__faturas = inst

    
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
            # lógica para confirmar a senha mesmo (IF ->>> cancelar_acao)
            fechar_dialogo()
            if ao_confirmar:
                ao_confirmar()

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
                    ft.Row([ft.Text("Confirme sua senha"), confirmar_senha], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=15)
            ),
            actions=[confirmar, ft.TextButton("Cancelar", on_click=cancelar_acao)]
        )
        self.page.dialog = dialogo
        self.page.open(dialogo)
        self.page.update()

    
    def confirmar(self, aviso : str = '', ao_confirmar : callable = None, ao_cancelar : callable = None) -> bool:

        dialogo = None

        def fechar_dialogo(e = None):
            nonlocal dialogo
            self.page.close(dialogo)
            self.page.update()

        def confirmar_acao(e=None):
            fechar_dialogo()
            if ao_confirmar:
                ao_confirmar()

        def cancelar_acao(e=None):
            fechar_dialogo()
            if ao_cancelar:
                ao_cancelar

        sim = ft.TextButton("Sim", on_click = confirmar_acao)
        nao = ft.TextButton("Não", on_click = cancelar_acao)

        dialogo = ft.AlertDialog(
            modal=True, title=ft.Text("Confirmar Ação", weight=ft.FontWeight.BOLD), bgcolor=self.cor_dialogo,
            content=ft.Container(width=250, height=70, padding=20, content=ft.Column([ft.Text(aviso)])),
            actions=[sim, nao]
        )
        self.page.dialog = dialogo
        self.page.open(dialogo)
        self.page.update()


    def pagina_principal(self) -> None:
        
        # Limpa a tela (anteriormente: login)
        self.page.clean()

        # Lista de botões do menu lateral
        botoes_menu = [("Clientes", ft.Icons.GROUPS), ("Solicitações", ft.Icons.CHECKLIST), ("Planos", ft.Icons.LIST_ALT),
                    ("Cadastrar cliente", ft.Icons.GROUP_ADD), ("Cadastrar número", ft.Icons.PHONE), ("---DIVISOR---", None), ("Sair", ft.Icons.LOGOUT)]
        

        # Criando os botões do menu
        menu_controls = []

        for texto, icone in botoes_menu:
            if texto == "---DIVISOR---":
                menu_controls.append(ft.Divider(thickness=1, color="gray"))
            else:
                menu_controls.append(
                    ft.TextButton(
                        text = texto, icon = icone, on_click = self.paginas_menu_lateral, width = 200, height = 45,
                        style = ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=4), alignment=ft.alignment.center_left, padding=10)
                    )
                )
        # Menu lateral
        menu = ft.Container(
            content = ft.Column(controls = menu_controls, spacing=5, expand=False),
            padding = ft.padding.symmetric(horizontal=10, vertical=15),
            bgcolor = ft.Colors.with_opacity(0.01, ft.Colors.BLUE_GREY),
            border_radius = 10,
        )
        # Cabeçalho (Faixa de cima da página)
        cabecalho = ft.Container(
            content = ft.Text("Área do Administrador", size=20, weight=ft.FontWeight.BOLD, color="white"),
            padding = 20,
            alignment = ft.alignment.center,
        )
        # Layout principal
        layout = ft.Column([
            cabecalho,
            ft.Row([menu, ft.VerticalDivider(width=1), self.conteudo_pagina], expand=True, alignment=ft.alignment.top_left)
            ],
            expand=True
        )
        # Cria a página:
        self.page.add(layout)
        self.pagina_clientes()


    def paginas_menu_lateral(self, e : ft.ControlEvent) -> None:
        match  e.control.text:
            case 'Cadastrar cliente':   self.cadastros.cadastrar_cliente()
            case 'Clientes':            self.pagina_clientes()
            case 'Cadastrar número':    self.cadastros.cadastrar_numero()
            case 'Solicitações':        self.solicitacoes.pagina_solicitacoes()
            case 'Planos':              self.planos.pagina_planos()
            case 'Sair':                self.sair()



    def criar_cartao_cliente(self, cliente):
        return ft.Container(
            bgcolor = self.cor_cartao_3, alignment= ft.alignment.top_left, border_radius = 5, padding = 10, border=ft.border.all(1), width=280,
            content=ft.Column([
                # Topo com ícone e email
                ft.Row([ ft.Icon(ft.Icons.PERSON, size=30), ft.Text(cliente["email"], weight=ft.FontWeight.BOLD) ]),
                ft.Divider(),
                # Área de números com botão editar
                ft.Container( bgcolor = self.cor_cartao_1, border_radius = 10, padding = 10,
                    content = ft.Column([
                        ft.Text("Números", weight=ft.FontWeight.BOLD),
                            *[
                                ft.Row([ ft.Text(numero, expand=True), self.criar_botao('Editar', cor=False, funcao=self.pagina_edicao_numero)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                                for numero in cliente["numeros"]
                            ]
                    ])
                ),
                ft.Container( alignment=ft.alignment.center,  padding=10,
                    content= ft.Row([self.criar_botao('Ver faturas', funcao=self.faturas.ver_faturas_cliente),
                                    self.criar_botao('Adicionar número', funcao=self.cadastros.cadastrar_numero)],
                                    spacing = 10, alignment=ft.alignment.center)
                )], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
    

    def pagina_clientes(self) -> None:

        cabecalho = ft.Container(content=ft.Column([
            ft.Row(  [ ft.Row([ft.Icon(ft.Icons.PHONE),ft.Text("Clientes cadastrados", size = 22, weight = ft.FontWeight.BOLD)]),
                       ft.Row([self.criar_botao("Cadastrar cliente", icone=ft.Icons.ADD, funcao=self.cadastros.cadastrar_cliente)])], spacing = 15, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]))

        self.atualizar_pagina(
            ft.Column( controls = [ cabecalho, ft.Divider(thickness=2),
                ft.Row( wrap=True, spacing=20, run_spacing=20, expand = True, scroll = ft.ScrollMode.AUTO,
                        controls=[self.criar_cartao_cliente(c) for c in clientes])
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

        novo_proprieatorio = self.dropdown(tamanho=220, listaOpcoes=cpfs)
        novo_proprieatorio.on_change = on_change_novo_proprieatario
        novo_proprieatorio.label = "CPF"
        novo_plano = self.dropdown(tamanho=220, listaOpcoes=planos)
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
                    self.criar_botao('Suspender número', cor=False,
                                     funcao = lambda e: self.confirmar(aviso="O número será suspenso após análise.", ao_confirmar=self.suspender_numero)),
                    self.criar_botao('Cancelar número', cor=False,
                                     funcao= lambda e : self.confirmar_identidade(titulo='Cancelar número', ao_confirmar=self.cancelar_numero))
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
        salvar = self.criar_botao("Salvar")
        cancelar = self.criar_botao("Cancelar", funcao=self.pagina_edicao_numero)

        self.atualizar_pagina(
            ft.Column(scroll = ft.ScrollMode.AUTO, controls=[
                cabecalho, ft.Divider(thickness=2), ft.Column([ft.Row([campo1, campo2]), ft.Row([salvar, cancelar])], spacing=25)]
            )
        )


    def suspender_numero(self, e:ft.ControlEvent = None) -> None:
        
        print("Iá suspender o número")


    def cancelar_numero(self, e:ft.ControlEvent = None) -> None:

        print("Irá cancelar o número")