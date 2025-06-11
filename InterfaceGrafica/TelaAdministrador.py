import flet as ft
from InterfaceGrafica.TelaBase import TelaBase

clientes = [
    {"email": "filipe@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666", "5555555555"]},
    {"email": "gaskdjasd@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "akkaka@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "matheus@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "gabriel@gmail.com", "numeros": ["9999999999", "8888888888"]},
]


class TelaAdministrador(TelaBase):

    def __init__(self, page : ft.Page, login_callback):

        super().__init__(page = page, login_callback = login_callback)
        self.conteudo_pagina_principal.alignment = ft.alignment.top_left


    def pagina_principal(self) -> None:
        
        self.page.clean()           # Limpa a tela
        self.pagina_clientes()      # Tela padrão : clientes
        
        # Função para tratar clique nos botões
        def menu_click(e):
            texto = e.control.text
            match  texto:
                case 'Clientes':        self.pagina_clientes()
                case 'Solicitações':    self.pagina_solicitacoes()
                case 'Planos':          self.pagina_planos()
                case 'Sair':            self.sair()

        # Lista de botões do menu lateral
        botoes_menu = ["Clientes", "Solicitações", "Planos", "---DIVISOR---",  "Sair"]
        
        # Lista de ícones do menu lateral
        lista_icones_botoes = [ ft.Icons.SUPERVISOR_ACCOUNT, ft.Icons.CHECKLIST, ft.Icons.LIST_ALT, None, ft.Icons.EXIT_TO_APP]

        # Criando os botões do menu
        menu_controls = []

        for texto, icone in zip(botoes_menu, lista_icones_botoes):
            if texto == "---DIVISOR---":
                menu_controls.append(ft.Divider(thickness=1, color="gray"))
            else:
                menu_controls.append(
                    ft.TextButton(
                        text = texto, icon = icone,
                        on_click = menu_click,
                        width = 200, height = 45,
                        style = ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=4), alignment=ft.alignment.center_left, padding=10
                        )
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
            ft.Row([menu, ft.VerticalDivider(width=1), self.conteudo_pagina_principal], expand=True, alignment=ft.alignment.top_left)
            ],
            expand=True
        )
        # Cria a página:
        self.page.add(layout)


    def criar_cartao_cliente(self, cliente):
        return ft.Container(
            bgcolor = self.cor_cartao_3,
            alignment= ft.alignment.top_left,
            width = 250, padding = 10, border=ft.border.all(1, "black"),
            content=ft.Column([
                # Topo com ícone e email
                ft.Row([
                    ft.Icon(ft.Icons.PERSON, size=30),
                    ft.Text(cliente["email"], weight=ft.FontWeight.BOLD)
                ]),
                ft.Divider(),

                # Área de números com botão editar
                ft.Container(
                    bgcolor = self.cor_cartao_1, border_radius = 10, padding = 10,
                    content = ft.Column([
                        ft.Text("Números", weight=ft.FontWeight.BOLD),
                        *[
                            ft.Row([
                                ft.Text(numero, expand=True),
                                ft.ElevatedButton("Editar", style=ft.ButtonStyle(padding=5, bgcolor= self.cor_botao, color="white"), height=30)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                            for numero in cliente["numeros"]
                        ]
                    ])
                ),
                # Botão 'Ver faturas'
                ft.Container(
                    alignment=ft.alignment.center,  padding=10,
                    content=ft.ElevatedButton("Ver faturas", bgcolor = self.cor_botao, color="white")
                )])
        )

    def pagina_clientes(self) -> None:
        self.conteudo_pagina_principal.content = ft.Row(
            wrap=True, spacing=20, run_spacing=20, expand = True, scroll = ft.ScrollMode.AUTO,
            controls=[self.criar_cartao_cliente(c) for c in clientes], alignment = ft.alignment.top_left
        )
        self.page.update()


    def pagina_solicitacoes(self) -> None:
        
        # Exemplo de dados
        dados = [
            {"numero": "001", "solicitante": "João", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
            {"numero": "002", "solicitante": "Maria", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
            {"numero": "003", "solicitante": "Pedro", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
            {"numero": "004", "solicitante": "Ana", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
        ]

        self.conteudo_pagina_principal.content = ft.Container(
            expand=True,
            padding=10,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Row(
                        wrap = True, spacing = 20, run_spacing = 20,
                        controls=[
                            self.criar_cartao_solicitacao(
                                d["numero"], d["solicitante"], d["descricao"], d["status"]
                            )
                            for d in dados
                        ]
                    )
            ]
        ))
        self.page.update()


    def criar_cartao_solicitacao(self, numero, solicitante, descricao, status) -> ft.Container:

        status_text = ft.Text(status, color=ft.Colors.WHITE)

        def on_status_change(novo_status):
            status_text.value = novo_status
            status_text.update()
            
        menu = ft.PopupMenuButton(
            padding = 5,
            content = status_text,
            items=[
                ft.PopupMenuItem(text="Pendente", on_click = lambda _: on_status_change("Pendente")),
                ft.PopupMenuItem(text="Resolvida", on_click = lambda _: on_status_change("Resolvida")),
            ],
            bgcolor = self.cor_botao
        )
        return ft.Container(
            width=250,
            border=ft.border.all(1),
            border_radius=5,
            content=ft.Column([
                # Cabeçalho sem padding lateral
                ft.Container(
                    width=float("inf"),
                    bgcolor=self.cor_cartao_2,
                    padding=ft.padding.all(10),
                    content=ft.Text(f"Solicitação ({numero})", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    alignment=ft.alignment.center
                ),
                # Corpo com padding interno
                ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Container(
                            width=float("inf"), border=ft.border.all(1), padding=ft.padding.all(5),
                            margin=ft.margin.only(bottom=5),
                            content=ft.Row([
                                ft.Text("Solicitante:", weight=ft.FontWeight.BOLD),
                                ft.Text(solicitante)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ),
                        ft.Container(
                            width=float("inf"), border=ft.border.all(1), padding=5,
                            margin=ft.margin.only(bottom=5),
                            content=ft.Text(f"Tipo: {descricao}", size=12)
                        ),
                        ft.Row([
                            ft.Text("Status:", weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content = menu, bgcolor = self.cor_botao,
                                padding = ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius = 10, alignment = ft.alignment.center
                            )
                        ], alignment=ft.MainAxisAlignment.END)
                    ])
                )
            ])
        )
    

    def pagina_planos(self) -> None:
        
        def editar(e):
            pass
        def excluir(e):
            pass    
        
        dados = [
            {"nome": "PLANO 1", "valor": "29,30", "dados": 64, "recarga": "15", "max_ligacoes": 10, "max_mensagens": 100, "clientes_usuarios": "45"},
            {"nome": "PLANO 2", "valor": "39,30", "dados": 90, "recarga": "15", "max_ligacoes": 15, "max_mensagens": 100, "clientes_usuarios": "25"},
            {"nome": "PLANO 3", "valor": "49,30", "dados": 100, "recarga": "15", "max_ligacoes": 15, "max_mensagens": 150, "clientes_usuarios": "15"}
        ]

        self.conteudo_pagina_principal.content = ft.Container(
            expand = True, padding=10,
            content = ft.Column(
                expand = True,
                scroll = ft.ScrollMode.AUTO,
                controls = [
                    ft.Row(
                        wrap = True, spacing = 20, run_spacing = 20,
                        controls=[
                            self.criar_cartao_plano(
                                d["nome"], d["valor"], d["dados"], d["recarga"], d["max_ligacoes"], d["max_mensagens"], d["clientes_usuarios"], self.pagina_editar_plano , excluir
                            )
                            for d in dados
                        ]
                    )
            ]
        ))
        self.page.update()


    def criar_cartao_plano(self, nome_plano, valor, dados_internet, valor_recarga, max_ligacoes, max_mensagens, clientes_usuarios, on_editar, on_excluir):

        def linha(label, valor):
            return ft.Container(
                padding=5,
                border=ft.border.only(bottom=ft.BorderSide(1)),
                content=ft.Row([
                    ft.Text(label, size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(valor, size=14),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
        return ft.Container(
            width=300, border=ft.border.all(2), border_radius=5,
            content=ft.Column([
                # Cabeçalho
                ft.Container(
                    bgcolor= self.cor_cartao_2, padding=ft.padding.all(10), alignment=ft.alignment.center, width=float("inf"),
                    content=ft.Text(nome_plano, color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD)
                ),
                # Informações
                ft.Container(
                    padding=5, border=ft.border.all(1),
                    content=ft.Column([
                        linha("VALOR:", f"R$ {valor}"),
                        linha("DADOS DE INTERNET", f"{dados_internet} GB"),
                        linha("VALOR RECARGA:", f"R$ {valor_recarga}"),
                        linha("MÁXIMO DE LIGAÇÕES", str(max_ligacoes)),
                        linha("MÁXIMO DE MENSAGENS", str(max_mensagens)),
                        linha("CLIENTES USUÁRIOS", str(clientes_usuarios)),
                    ])
                ),
                # Botões
                ft.Container(padding=ft.padding.only(top=2, left=10, right=10, bottom=10) ,content=
                    ft.Row([
                        ft.ElevatedButton("Editar", on_click = on_editar, bgcolor = self.cor_botao, color = ft.Colors.WHITE,
                                        style=ft.ButtonStyle( padding=ft.padding.symmetric(vertical=15, horizontal=30))),
                        ft.ElevatedButton("Excluir", on_click = on_excluir, bgcolor = self.cor_botao, color = ft.Colors.WHITE,
                                        style=ft.ButtonStyle( padding=ft.padding.symmetric(vertical=15, horizontal=30)))
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=10, expand=True)
                )
            ])
        )
    
    def pagina_editar_plano(self, e = None) -> None:

        # Cabeçalho
        cabecalho = ft.Container(
            padding=ft.padding.symmetric(vertical=10, horizontal=10),
            content=ft.Text("Edição: Plano X", weight=ft.FontWeight.BOLD, size=22, color=ft.Colors.WHITE), expand=True,
        )

        # Função para criar as linhas com bordas e alinhamento
        def linha_com_borda(label, textfield):
            return ft.Container(
                padding=10, height=60, border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.BLACK)),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(label, weight=ft.FontWeight.BOLD), textfield
                    ],
                )
            )

        # Campos editáveis
        valor = linha_com_borda("VALOR:", ft.TextField(width=130, prefix_text="R$ ", text_size = 11))
        dados_internet = linha_com_borda("DADOS DE INTERNET:", ft.TextField(width=130, suffix_text=" GB", text_size = 11))
        valor_recarga = linha_com_borda("VALOR RECARGA:", ft.TextField(width=130, prefix_text="R$ ", text_size = 11))
        max_ligacoes = linha_com_borda("MÁXIMO DE LIGAÇÕES:", ft.TextField(width=130, text_size = 11))
        max_msg = linha_com_borda("MÁXIMO DE MENSAGENS:", ft.TextField(width=130, text_size = 11))

        # Container com borda geral e arredondada para o bloco de edição
        dados_editaveis = ft.Container(
            width=400, border=ft.border.all(1), border_radius=10,
            content=ft.Column( controls=[ valor, dados_internet, valor_recarga, max_ligacoes, max_msg, ], spacing=0,
            )
        )

        # Função para criar cada usuário
        def usuario_item(email):
            return ft.Container(
                height=60,
                border=ft.border.all(1, ft.Colors.BLACK),
                padding=10,
                content=ft.Row(
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.PERSON),
                        ft.Text(email)
                    ],
                )
            )

        # Lista simulada com 4 usuários
        usuarios = ft.Column(
            controls=[
                usuario_item("filipe1@gmail.com"),
                usuario_item("filipe2@gmail.com"),
                usuario_item("filipe3@gmail.com"),
                usuario_item("filipe4@gmail.com"),
            ],
            spacing=0,
        )

        # Lista de clientes usuários com título e bordas iguais a da imagem
        titulo_clientes = ft.Container(
            height = 40, border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.BLACK)), padding = 10,
            content=ft.Text("CLIENTES USUÁRIOS", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        )

        clientes_usuarios = ft.Container(
            width=300, height=320, border=ft.border.all(1), border_radius=10,
            content=ft.Column( controls=[titulo_clientes, usuarios], spacing=0,)
        )

        # Botões Salvar e Cancelar alinhados à esquerda
        botoes = ft.Row(
            controls=[
                ft.ElevatedButton("Salvar", bgcolor=self.cor_botao, color=ft.Colors.WHITE),
                ft.ElevatedButton("Cancelar", bgcolor=self.cor_botao, color=ft.Colors.WHITE),
            ],
            spacing=8, alignment=ft.MainAxisAlignment.START,
        )

        # Conteúdo principal
        self.conteudo_pagina_principal.content = ft.Column(
            controls=[
                cabecalho,
                ft.Divider(thickness=2),
                ft.Row(
                    controls=[dados_editaveis, clientes_usuarios],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=30),  # espaço antes dos botões
                botoes,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            expand=True, scroll=ft.ScrollMode.AUTO
        )
        self.conteudo_pagina_principal.update()