import flet as ft
from InterfaceGrafica.TelaUsuario import TelaUsuario


class TelaCliente(TelaUsuario):

    def __init__(self, page : ft.Page, login_callback):

        super().__init__(page = page, login_callback = login_callback)
        self.__menu_lateral = ft.Column(spacing = 5, expand = False)
        self.numeros = ['(31) 91234-5678', '(31) 99876-5432', '(31) 93456-7890']
        self.planos = []

        # Usando Ref para acessar o container (possibilita animações)
        self.numeros_expandiveis_ref = ft.Ref[ft.Container]()
        self.numeros_lista_ref = ft.Ref[ft.Column]()
        self.__numeros_expandiveis = ft.Container(
            content=ft.Column(ref=self.numeros_lista_ref, spacing=5), height=0, animate=ft.Animation(duration=300, 
            curve=ft.AnimationCurve.EASE_IN_OUT), clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ref = self.numeros_expandiveis_ref, )

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
                       ("Faturas", ft.Icons.PAYMENT), ("Ajuda / Suporte", ft.Icons.HELP), ("DIVISOR", None), ("Sair", ft.Icons.EXIT_TO_APP)]
        
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
            case 'Editar dados':        self.pagina_editar_dados()
            case 'Meus Números':        self.exibir_numeros()
            case 'Adicionar Número':    self.adicionar_numero()
            case 'Faturas':             self.faturas()
            case 'Ajuda / Suporte':     self.ajuda_suporte()
            case 'Sair':                self.sair()

    def pagina_editar_dados(self) -> None:

        cabecalho = ft.Container(content=ft.Row([
            ft.Column([ft.Text("Editar Dados", size=22, weight=ft.FontWeight.BOLD), ft.Text("CPF: XXX.XXX.XXX-XX")], spacing = 10, expand = True, alignment=ft.alignment.top_left),
            ft.Column([ft.Row([ 
                self.criar_botao('Anexar foto', cor=False),
                ft.Icon(ft.Icons.ACCOUNT_BOX, size = 60) ], spacing = 6)], alignment=ft.alignment.top_right),
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
                [self.criar_botao("Alterar email"), self.criar_botao("Alterar senha")]),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=50,))

        self.atualizar_pagina(ft.Column([cabecalho, ft.Divider(thickness=2), campo], scroll=ft.ScrollMode.AUTO))


    def exibir_numeros(self) -> None:
        
        container = self.numeros_expandiveis_ref.current
        coluna = self.numeros_lista_ref.current

        if container.height == 0:
            # Expandir
            coluna.controls = [
                ft.TextButton(
                    text=num, icon=ft.Icons.CHEVRON_RIGHT,
                    on_click= self._numero_clicado, width=200, height=40,
                    style = ft.ButtonStyle(
                        padding = 5,
                        alignment = ft.alignment.center_left,
                        shape = ft.RoundedRectangleBorder(radius=4),
                        bgcolor= ft.Colors.with_opacity(0.04, ft.Colors.ON_SURFACE)
                    )
                )
                for num in self.numeros
            ]
            container.height = len(self.numeros) * 45 + 10
        else:
            # Colapsar
            container.height = 0

        container.update()


    def _numero_clicado(self, e):
        
        def card_titulo(texto : str = '', icone : ft.Icon = None) -> ft.Row:
            return ft.Row([ft.Icon(icone, size = 24), ft.Text(texto, size = 18, weight = ft.FontWeight.BOLD)])

        def linha_info(texto : str = '', info : str = '') -> ft.Row:
            return(ft.Row([ft.Text(texto), ft.Text(info, size=14, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

        def barra_progresso(progresso_percentual : float = 0.0) -> ft.ProgressBar:
            return(ft.ProgressBar(value=progresso_percentual/100, 
                    height=10, color=self.cor_barra_progresso, bgcolor=self.cor_cartao_2, width=float('inf')))

        cabecalho = ft.Row([
            ft.Column([ ft.Text(e.control.text, size=22, weight=ft.FontWeight.BOLD),
                        ft.Row([ft.Text("Nome do plano", size=16), self.criar_botao("Ver detalhes", cor=False)], spacing = 10),
                        ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH),ft.Text("Ativo desde: XX/XX/2025")], spacing = 5),
                        ft.Row([ft.Icon(ft.Icons.DONE), ft.Text("Status: Ativa")], spacing = 5),
                        ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY),ft.Text("Próxima fatura: R$ 45,90 - Vence: XX/XX/2025")], spacing = 5),
                        ],spacing = 10, expand = True, alignment=ft.alignment.top_left),
            ft.Column([ self.criar_botao("Cancelar número", ft.Icons.CANCEL),
                        self.criar_botao("Transferir número", ft.Icons.COMPARE_ARROWS),
                        self.criar_botao("Mudar assinatura (Plano)")],
                        alignment=ft.alignment.top_right)
        ])
        internet = ft.Container(
            padding = 15, border = ft.border.all(2), border_radius = 10,
            content = ft.Column([
                card_titulo("INTERNET", ft.Icons.WIFI),
                ft.Text(f"{73}% utilizados ({730} MB de {1000} MB)"),
                barra_progresso(73),
                ft.Row([self.criar_botao("Comprar pacote extra", ft.Icons.ADD),
                        self.criar_botao("Ver consumo", ft.Icons.LIST_ALT)],
                       alignment=ft.MainAxisAlignment.START, spacing = 10),
            ])
        )
        minutos = ft.Container(
            padding = 15, border = ft.border.all(2), border_radius = 10,
            content=ft.Column([
                card_titulo("MINUTOS", ft.Icons.PHONE),
                ft.Text(f"{60}% utilizados (6 ligações - 37/60 min)"),
                linha_info("Renova em", "11/07/2025"),
                barra_progresso(60),
                ft.Row([self.criar_botao("Adicionar minutos", ft.Icons.ADD),
                        self.criar_botao("Ver ligações", ft.Icons.LIST_ALT)],
                       alignment=ft.MainAxisAlignment.START, spacing = 10),
            ])
        )
        mensagens = ft.Container(
            padding = 15, border = ft.border.all(2), border_radius=10,
            content=ft.Column([
                card_titulo("MENSAGENS", ft.Icons.MESSAGE),
                ft.Text(f"{40} de 100 mensagens utilizados ({60} disponíveis)"),
                linha_info("Renova em", "11/07/2025"),
                barra_progresso(40),
                ft.Row([self.criar_botao("Comprar pacote de mensagens", ft.Icons.ADD),
                        self.criar_botao("Ver histórico", ft.Icons.LIST_ALT)],
                       alignment=ft.MainAxisAlignment.START, spacing = 10),
            ])
        )
        saldos = ft.Container(
            padding = 15, border = ft.border.all(2), border_radius = 10,
            content = ft.Column([
                card_titulo("SALDOS", ft.Icons.ATTACH_MONEY),
                linha_info("Saldo atual", f"{0.0}"),
                linha_info("Última recarga", "11/06/2025"),
                linha_info("Expira em", "11/07/2025"),
                ft.Row([self.criar_botao("Fazer recarga", ft.Icons.ADD),
                        self.criar_botao("Ver histórico", ft.Icons.LIST_ALT)],
                       alignment=ft.MainAxisAlignment.START, spacing = 10),
            ])
        )

        self.atualizar_pagina(
            ft.Column(
            [cabecalho, ft.Divider(thickness=2),
             ft.Row([
             ft.Column([internet, mensagens], expand = True, alignment = ft.MainAxisAlignment.START, width = 450), 
             ft.Column([minutos, saldos], expand = True, alignment = ft.MainAxisAlignment.START, width = 450)], expand = True
             , alignment = ft.alignment.top_left)], spacing=20, scroll=ft.ScrollMode.AUTO
            )
        )


    def adicionar_numero(self) -> None:

        cabecalho = ft.Text("Adicionar novo número", size=22, weight=ft.FontWeight.BOLD)

        plano_selecionado = ft.Text("")
        recarga_valor = ft.Text("")

        # Radio group de recarga
        recarga_group = ft.RadioGroup(
            content = ft.Row([
                ft.Radio(value="10", label="R$ 10,00"), ft.Radio(value="20", label="R$ 20,00"),
                ft.Radio(value="30", label="R$ 30,00"), ft.Radio(value="40", label="R$ 40,00"),])
        )

        def selecionar_plano(e):
            
            # Reseta seleção de plano
            for plano in self.planos:
                plano.border = ft.border.all(1)
                plano.bgcolor = ft.Colors.TRANSPARENT

            e.control.border = ft.border.all(3, self.cor_botao)
            e.control.bgcolor = ft.Colors.with_opacity(0.1, self.cor_barra_progresso)
            plano_selecionado.value = f"Plano selecionado: {e.control.data}"
            self.page.update()

        def solicitar_numero(e):
            valor_recarga = recarga_group.value
            plano = plano_selecionado.value
            recarga_valor.value = f"Recarga escolhida: R$ {valor_recarga}, {plano}"
            self.page.update()


        plano1 = ft.Container(
            content=ft.Column([
                ft.Container(
                    bgcolor= self.cor_cartao_2, padding=ft.padding.all(5), alignment=ft.alignment.center, width=float("inf"),
                    content=ft.Text("Plano 1", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD), border=ft.border.all(1), border_radius=10
                ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Internet"), ft.Text("5 GB")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Minutos"), ft.Text("100")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Mensagens"), ft.Text("50")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Valor Mensal"), ft.Text("R$ 49,90")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) )
            ], horizontal_alignment=ft.CrossAxisAlignment.START),
            border=ft.border.all(1), border_radius=10, expand = True, on_click = selecionar_plano,  data="PLANO 1"
        )
        plano2 = ft.Container(
            content=ft.Column([
                ft.Container(
                    bgcolor= self.cor_cartao_2, padding=ft.padding.all(5), alignment=ft.alignment.center, width=float("inf"),
                    content=ft.Text("Plano 2", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD), border=ft.border.all(1), border_radius=10
                ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Internet"), ft.Text("4 GB")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Minutos"), ft.Text("90")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Mensagens"), ft.Text("50")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Valor Mensal"), ft.Text("R$ 39,90")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) )
            ], horizontal_alignment=ft.CrossAxisAlignment.START),
            border=ft.border.all(1), border_radius=10, expand = True, on_click = selecionar_plano,  data="PLANO 2"
        )

        plano3 = ft.Container(
            content=ft.Column([
                ft.Container(
                    bgcolor= self.cor_cartao_2, padding=ft.padding.all(5), alignment=ft.alignment.center, width=float("inf"),
                    content=ft.Text("Plano 3", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD), border=ft.border.all(1), border_radius=10
                ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Internet"), ft.Text("8 GB")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Minutos"), ft.Text("120")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Mensagens"), ft.Text("100")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) ),
                ft.Container( padding=8,
                             content = ft.Row([ft.Text("Valor Mensal"), ft.Text("R$ 69,90")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) )
            ], horizontal_alignment=ft.CrossAxisAlignment.START),
            border=ft.border.all(1), border_radius=10, expand = True, on_click = selecionar_plano, data="PLANO 3"
        )

        self.planos = [plano1, plano2, plano3]

        self.atualizar_pagina(
            ft.Column([
                cabecalho,
                ft.Divider(thickness=2),
                ft.Container( content=ft.Column([
                        ft.Text("Escolha seu plano", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([plano1, plano2, plano3], alignment=ft.MainAxisAlignment.START),
                    ]),
                    padding=10, border=ft.border.all(1), border_radius=10, margin=10
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Recarga inicial", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([ ft.Text("Valor: "), recarga_group ])
                    ]),
                    padding=10, border=ft.border.all(1), border_radius=10, margin=10
                ),
                ft.Row([
                    ft.ElevatedButton("Solicitar número", on_click = solicitar_numero, bgcolor = self.cor_botao),
                    ft.ElevatedButton("Cancelar", on_click = lambda e: self.pagina_principal(), bgcolor = self.cor_botao)
                ]),
                plano_selecionado,
                recarga_valor], scroll=ft.ScrollMode.AUTO
            )
        )

    def faturas(self) -> None:

        numero_selecionado = ft.Ref[ft.Dropdown]()
        mes_selecionado = ft.Ref[ft.Dropdown]()
        container_detalhes = ft.Ref[ft.Container]()

        def atualizar_fatura(e = None):
            if not numero_selecionado.current.value or not mes_selecionado.current.value:
                return
            container_detalhes.current.content = ft.Column([
                ft.Text("Fatura da linha", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"Número: {numero_selecionado.current.value}", size=16),
                ft.Text(f"Referente a: {mes_selecionado.current.value}", size=16),
                ft.Divider(thickness=1),
                ft.Text("Valor total: R$ 79,90", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("Vencimento: 10/06/2025", size=14),
                ft.Divider(),
                ft.Row([
                    ft.OutlinedButton("Pagar com Pix", icon=ft.Icons.PIX, on_click=lambda e: print("Pagamento com Pix")),
                    ft.OutlinedButton("Exibir código de barras", icon=ft.Icons.VIEW_HEADLINE, on_click=lambda e: print("Exibindo código de barras")),
                ], spacing=15),
                ft.Divider(),
                ft.Text("Detalhes da Fatura", size=16, weight=ft.FontWeight.BOLD),
                ft.ListTile(title=ft.Text("Plano mensal"), trailing=ft.Text("R$ 49,90")),
                ft.ListTile(title=ft.Text("Internet extra"), trailing=ft.Text("R$ 20,00")),
                ft.ListTile(title=ft.Text("Impostos e taxas"), trailing=ft.Text("R$ 10,00")),
            ])
            container_detalhes.current.update()

        meses = ["06/2025", "05/2025", "04/2025", "03/2025"]

        numero_dropdown = ft.Dropdown(
            label="Escolha um número", options=[ft.dropdown.Option(n) for n in self.numeros],
            on_change = atualizar_fatura, ref=numero_selecionado, width=300,
        )
        mes_dropdown = ft.Dropdown(
            label="Mês de Referência", options = [ft.dropdown.Option(m) for m in meses],
            on_change = atualizar_fatura, ref = mes_selecionado, width=300,
        )

        self.atualizar_pagina(
            ft.Column([
                ft.Text("Faturas", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(thickness=2),
                ft.Row([numero_dropdown, mes_dropdown], spacing=20),
                ft.Container(ref=container_detalhes, padding=10)
                ], spacing=20, scroll=ft.ScrollMode.AUTO
            )
        )

            
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