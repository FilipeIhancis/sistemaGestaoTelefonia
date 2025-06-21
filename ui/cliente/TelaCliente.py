import flet as ft
from ui.base.TelaUsuario import TelaUsuario
from ui.cliente.PaginaFaturas import PaginaFaturas
from ui.cliente.PaginaNumeros import PaginaNumeros
from ui.cliente.PaginaAdicionarNumero import PaginaAdicionarNumero
from models.cliente import Cliente

class TelaCliente(TelaUsuario):

    def __init__(self, page : ft.Page, login_callback, usuario : Cliente):

        super().__init__(page = page, login_callback = login_callback, usuario=usuario)
        self.__menu_lateral = ft.Column(spacing = 5, expand = False)
        self.numeros_fake = ['(31) 91234-5678', '(31) 99876-5432', '(31) 93456-7890']
        self.planos_fake = []

        # Usando Ref para acessar o container (possibilita animações)
        self.numeros_expandiveis_ref = ft.Ref[ft.Container]()
        self.numeros_lista_ref = ft.Ref[ft.Column]()
        self.__numeros_expandiveis = ft.Container(
            content=ft.Column(ref=self.numeros_lista_ref, spacing=5), height=0, animate=ft.Animation(duration=300, 
            curve=ft.AnimationCurve.EASE_IN_OUT), clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ref = self.numeros_expandiveis_ref, )
        
        self.__faturas = PaginaFaturas(self)
        self.__numeros = PaginaNumeros(self)
        self.__adicionar_numero = PaginaAdicionarNumero(self)

    
    @property
    def adicionar_numero(self):
        return self.__adicionar_numero

    @adicionar_numero.setter
    def adicionar_numero(self, inst):
        if not isinstance(inst, PaginaAdicionarNumero):
            raise ValueError
        self.__adicionar_numero = inst

    @property
    def faturas(self):
        return self.__faturas
    
    @faturas.setter
    def faturas(self, inst):
        if not isinstance(inst, PaginaFaturas):
            raise ValueError("")
        self.__faturas = inst

    @property
    def numeros(self):
        return self.__numeros
    
    @numeros.setter
    def numeros(self, inst):
        if not isinstance(inst, PaginaNumeros):
            raise ValueError("")
        self.__numeros = inst

    @property
    def numeros_expandiveis(self):
        return self.__numeros_expandiveis
    
    @numeros_expandiveis.setter
    def numeros_expandiveis(self, container : ft.Container):
        if not isinstance(container, ft.Container):
            raise ValueError("Conteúdo inválido")
        self.__numeros_expandiveis = container
    
    @property
    def menu_lateral(self):
        return self.__menu_lateral
    
    @menu_lateral.setter
    def menu_lateral(self, coluna : ft.Column):
        if not isinstance(coluna, ft.Column):
            raise ValueError("Coluna inválida")
        self.__menu_lateral = coluna


    def pagina_principal(self) -> None:
        
        self.page.clean()   # Limpa a tela
    
        # Menu lateral
        menu = ft.Container(
            content = self.menu_lateral, padding=ft.padding.symmetric(horizontal=10, vertical=15),
            bgcolor=ft.Colors.with_opacity(0.01, ft.Colors.BLUE_GREY), border_radius=10,
        )
        # Cabeçalho (Faixa de cima da página)
        cabecalho = ft.Container(
            content = ft.Text("Área do Cliente", size=20, weight = ft.FontWeight.BOLD, color = "white"),
            padding = 20, alignment = ft.alignment.center,
        )
        # Cria o menu lateral da página
        self.criar_menu_lateral()

        # Layout principal
        layout = ft.Column([cabecalho, ft.Row([menu, ft.VerticalDivider(width=1), self.conteudo_pagina], expand=True)], expand=True)
        
        # Cria a página:
        self.page.add(layout)
    

    def criar_menu_lateral(self) -> None:

        botoes_menu = [('Editar dados', ft.Icons.MANAGE_ACCOUNTS), ("Meus Números", ft.Icons.PHONE), ("Adicionar Número", ft.Icons.PLUS_ONE),
                       ("Faturas", ft.Icons.PAYMENT), ("Ajuda / Suporte", ft.Icons.HELP), ("DIVISOR", None), ("Sair", ft.Icons.LOGOUT)]
        
        self.menu_lateral.controls.clear()

        for texto, icone in botoes_menu:
            if texto == "DIVISOR":
                self.menu_lateral.controls.append(ft.Divider(thickness=1, color="gray"))
                continue
            botao = ft.TextButton(
                text=texto, icon=icone, width=200, height=45, on_click = self.paginas_menu_lateral,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=4), alignment=ft.alignment.center_left, padding=10,
                )
            )
            self.menu_lateral.controls.append(botao)

            if texto == "Meus Números":
                self.menu_lateral.controls.append(self.numeros_expandiveis)
                

    def paginas_menu_lateral(self, e : ft.ControlEvent):
        match e.control.text:
            case 'Editar dados':        self.editar_dados.pagina_editar_dados()
            case 'Meus Números':        self.numeros.pagina_meus_numeros()
            case 'Adicionar Número':    self.adicionar_numero.pagina_adicionar_numero()
            case 'Faturas':             self.faturas.pagina_faturas()
            case 'Ajuda / Suporte':     self.ajuda_suporte()
            case 'Sair':                self.sair()

            
    def ajuda_suporte(self) -> None:
        
        cabecalho = ft.Container(content = ft.Column([ft.Text("Ajuda / Suporte", size = 22, weight = ft.FontWeight.BOLD),
                                                      ft.Text("Navegue pelos tópicos ou fale diretamente conosco.", size = 14)]))
        
        botoes_ajuda = ft.Container( padding = 10, expand = True, alignment=ft.alignment.top_left,
            content = ft.Column( spacing = 10, controls = [
                ft.ExpansionTile(title = ft.Text("Planos e assinaturas", weight = ft.FontWeight.BOLD),
                                 controls = [ft.Text("Dúvidas sobre upgrade")]),
                ft.ExpansionTile(title = ft.Text("Uso do número", weight = ft.FontWeight.BOLD),
                                 controls = [ft.Text("Dúvidas sobre upgrade")]),
                ft.ExpansionTile(title = ft.Text("Pagamentos e Faturas", weight = ft.FontWeight.BOLD),
                                 controls = [ft.Text("Dúvidas sobre upgrade")]),           
            ])
        )

        formulario = ft.Container(
            content = ft.Column([
                    ft.Text("Ajuda específica", weight = ft.FontWeight.BOLD, size = 18),
                    ft.TextField(label = "Assunto", border = ft.border.all(1, ft.Colors.GREY), border_color=ft.Colors.GREY),
                    ft.Dropdown(
                        label = "Categoria", border_color = ft.Colors.GREY, options=[
                            ft.dropdown.Option("Dúvida"),ft.dropdown.Option("Erro"),ft.dropdown.Option("Solicitação")
                        ]
                    ),
                    ft.TextField(label="Observações", multiline=True, min_lines=3,border=ft.border.all(1, ft.Colors.GREY),
                                 border_color=ft.Colors.GREY),
                    self.criar_botao("Enviar solicitação")
                ]), 
                padding = 20, border = ft.border.all(1), border_radius=10, expand = True, alignment=ft.alignment.top_left
        )

        self.atualizar_pagina(
            ft.Column(
                [cabecalho, ft.Divider(thickness=2),
                ft.Row(controls=[botoes_ajuda,formulario], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)],
                scroll = ft.ScrollMode.AUTO
            )
        )