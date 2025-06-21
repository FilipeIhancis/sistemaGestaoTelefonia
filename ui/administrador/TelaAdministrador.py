import flet as ft
from ui.base.TelaUsuario import TelaUsuario
from ui.administrador.PaginaSolicitacoes import PaginaSolicitacoes
from ui.administrador.PaginaCadastros import PaginaCadastro
from ui.administrador.PaginaPlanos import PaginaPlanos
from ui.administrador.PaginaFaturas import PaginaFaturas
from ui.administrador.PaginaClientes import PaginaClientes


class TelaAdministrador(TelaUsuario):

    def __init__(self, page : ft.Page, login_callback):
        super().__init__(page = page, login_callback = login_callback)

        self._cadastros = PaginaCadastro(self)
        self._clientes = PaginaClientes(self)
        self.__solicitacoes = PaginaSolicitacoes(self)
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
        return self._cadastros
    
    @cadastros.setter
    def cadastros(self, inst : PaginaCadastro):
        if not isinstance(inst, PaginaCadastro):
            raise ValueError("")
        self._cadastros = inst

    @property
    def clientes(self):
        return self._clientes
    
    @clientes.setter
    def clientes(self, inst:PaginaClientes):
        if not isinstance(inst, PaginaClientes):
            raise ValueError
        self._clientes = inst

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
        botoes_menu = [ ('Editar dados', ft.Icons.MANAGE_ACCOUNTS),
                        ("Clientes", ft.Icons.GROUPS),
                       ("Solicitações", ft.Icons.CHECKLIST),
                       ("Planos", ft.Icons.LIST_ALT),
                    ("Cadastrar cliente", ft.Icons.GROUP_ADD),
                    ("Cadastrar número", ft.Icons.PHONE),
                    ("---DIVISOR---", None),
                    ("Sair", ft.Icons.LOGOUT)]
        
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
        self.clientes.pagina_clientes()


    def paginas_menu_lateral(self, e : ft.ControlEvent) -> None:
        match  e.control.text:
            case 'Editar dados':        self.editar_dados.pagina_editar_dados()
            case 'Cadastrar cliente':   self.cadastros.cadastrar_cliente()
            case 'Clientes':            self.clientes.pagina_clientes()
            case 'Cadastrar número':    self.cadastros.cadastrar_numero()
            case 'Solicitações':        self.solicitacoes.pagina_solicitacoes()
            case 'Planos':              self.planos.pagina_planos()
            case 'Sair':                self.sair()