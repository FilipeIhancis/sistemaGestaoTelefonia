import flet as ft
from InterfaceGrafica.TelaBase import TelaBase


class TelaCliente(TelaBase):

    def __init__(self, page : ft.Page, login_callback):

        super().__init__(page = page, login_callback = login_callback)

        self.menu_lateral = ft.Column(spacing = 5, expand = False)

        self.numeros = ['(31) 91234-5678', '(31) 99876-5432', '(31) 93456-7890']

        # Usando Ref para acessar o container (possibilita animações)
        self.numeros_expandiveis_ref = ft.Ref[ft.Container]()
        self.numeros_lista_ref = ft.Ref[ft.Column]()
        self.numeros_expandiveis = ft.Container(
            content=ft.Column(ref=self.numeros_lista_ref, spacing=5), height=0, animate=ft.Animation(duration=300, 
            curve=ft.AnimationCurve.EASE_IN_OUT), clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ref = self.numeros_expandiveis_ref, )


    def pagina_principal(self) -> None:
        
        self.page.clean()   # Limpa a tela
    
        # Menu lateral
        menu = ft.Container(
            content = self.menu_lateral,
            padding=ft.padding.symmetric(horizontal=10, vertical=15),
            bgcolor=ft.Colors.with_opacity(0.01, ft.Colors.BLUE_GREY),
            border_radius=10,
        )
        # Cabeçalho (Faixa de cima da página)
        cabecalho = ft.Container(
            content = ft.Text("Área do Cliente", size=20, weight = ft.FontWeight.BOLD, color = "white"),
            padding = 20, alignment = ft.alignment.center,
        )
        # Cria o menu lateral da página
        self.criar_menu_lateral()

        # Layout principal
        layout = ft.Column([cabecalho, ft.Row([menu, ft.VerticalDivider(width=1), self.conteudo_pagina_principal], expand=True)], expand=True)
        
        # Cria a página:
        self.page.add(layout)
    

    def criar_menu_lateral(self) -> None:

        botoes_menu = [ ("Meus Números", ft.Icons.PHONE), ("Minhas Assinaturas", ft.Icons.LIST),
            ("Adicionar Número", ft.Icons.PLUS_ONE), ("Faturas", ft.Icons.PAYMENT),
            ("Ajuda / Suporte", ft.Icons.HELP), ("DIVISOR", None), ("Sair", ft.Icons.EXIT_TO_APP), ]
        
        self.menu_lateral.controls.clear()

        for texto, icone in botoes_menu:
            if texto == "DIVISOR":
                self.menu_lateral.controls.append(ft.Divider(thickness=1, color="gray"))
                continue
            botao = ft.TextButton(
                text=texto, icon=icone, width=200, height=45,
                on_click = self._menu_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=4), alignment=ft.alignment.center_left, padding=10,
                )
            )
            self.menu_lateral.controls.append(botao)

            if texto == "Meus Números":
                self.menu_lateral.controls.append(self.numeros_expandiveis)

    def _menu_click(self, e):
        texto = e.control.text
        match texto:
            case 'Meus Números':
                self.exibir_numeros()
            case 'Minhas Assinaturas':
                self.minhas_assinaturas()
            case 'Adicionar Número':
                self.adicionar_numero()
            case 'Transferir Número':
                self.transferir_numero()
            case 'Cancelar Número':
                self.cancelar_numero()
            case 'Faturas':
                self.faturas()
            case 'Ajuda / Suporte':
                self.ajuda_suporte()
            case 'Sair':
                self.sair()

    def exibir_numeros(self):
        
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
        
        def card_titulo(texto, icone):
            return ft.Row([ft.Icon(icone, size = 24), ft.Text(texto, size = 18, weight = ft.FontWeight.BOLD)])

        cabecalho = ft.Row([
            ft.Column([
                ft.Text(e.control.text, size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Nome do plano", size=16)], expand = True),
            ft.Column([
                ft.ElevatedButton("Cancelar número", bgcolor=self.cor_botao, color=ft.Colors.WHITE, 
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)), icon = ft.Icons.CANCEL),
                ft.ElevatedButton("Transferir número", bgcolor=self.cor_botao, color=ft.Colors.WHITE, 
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)), icon = ft.Icons.COMPARE_ARROWS),
            ], alignment=ft.MainAxisAlignment.END)
        ])
        internet = ft.Container(
            padding = 15,
            border = ft.border.all(2),
            border_radius = 10,
            content = ft.Column([
                card_titulo("INTERNET", ft.Icons.WIFI),
                ft.Text(f"{40}% utilizados"),
                ft.ProgressBar(value=40/100, height=10, color=self.cor_botao, bgcolor=self.cor_cartao_1, width=float('inf')),
                ft.Row([
                    ft.Text(f"Disponíveis: {400}/{1000}", size=12)
                ], alignment=ft.MainAxisAlignment.END)
            ])
        )
        minutos = ft.Container(
            padding = 15, border = ft.border.all(2), border_radius = 10,
            content=ft.Column([
                card_titulo("MINUTOS", ft.Icons.PHONE),
                ft.Text(f"{60}% utilizados"),
                ft.ProgressBar(value=60/100, height=10, color=self.cor_botao, bgcolor=self.cor_cartao_1, width=float('inf')),
                ft.Row([
                    ft.Text(f"Ligações realizadas: {6}", size=12),
                    ft.Text(f"Minutos disponíveis: {23}", size=12),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )
        mensagens = ft.Container(
            padding = 15, border = ft.border.all(2), border_radius=10,
            content=ft.Column([
                card_titulo("MENSAGENS", ft.Icons.MESSAGE),
                ft.Text(f"Total utilizado: {40} envios"),
                ft.Row([
                    ft.Text(f"Mensagens disponíveis: {60}", size=12)
                ], alignment=ft.MainAxisAlignment.END)
            ])
        )
        saldos = ft.Container(
            padding = 15, border = ft.border.all(2), border_radius = 10,
            content = ft.Column([
                card_titulo("SALDOS", ft.Icons.ATTACH_MONEY),
                ft.Row([
                    ft.Text("Recarga"),
                    ft.Text(f"R$ {0.0}", size=14, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )
        self.conteudo_pagina_principal.content = ft.Column(
            [cabecalho, ft.Divider(thickness=2),
             ft.Row([
             ft.Column([internet, mensagens], expand = True, alignment = ft.MainAxisAlignment.START, width = 450), 
             ft.Column([minutos, saldos], expand = True, alignment = ft.MainAxisAlignment.START, width = 450)], expand = True
             , alignment = ft.alignment.top_left)], spacing=20, scroll=ft.ScrollMode.AUTO
            )
        self.conteudo_pagina_principal.padding = 10
        self.conteudo_pagina_principal.alignment = ft.alignment.top_left
        self.conteudo_pagina_principal.update()


    def minhas_assinaturas(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Assinaturas!", size = 20)
        self.page.update()

    def adicionar_numero(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Vamos adicionar um novo número.", size = 20)
        self.page.update()


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

        self.conteudo_pagina_principal.content = ft.Column([
            ft.Text("Faturas", size=22, weight=ft.FontWeight.BOLD),
            ft.Divider(thickness=2),
            ft.Row([numero_dropdown, mes_dropdown], spacing=20),
            ft.Container(ref=container_detalhes, padding=10)
        ], spacing=20, scroll=ft.ScrollMode.AUTO)
        self.conteudo_pagina_principal.padding = 10
        self.conteudo_pagina_principal.alignment = ft.alignment.top_left
        self.conteudo_pagina_principal.update()

            
    def ajuda_suporte(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Ajuda do suporte.....", size = 20)
        self.page.update()
