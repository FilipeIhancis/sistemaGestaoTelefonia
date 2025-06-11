import flet as ft
import threading
from CoresTela import CoresTela

clientes = [
    {"email": "filipe@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666", "5555555555"]},
    {"email": "gaskdjasd@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "akkaka@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "matheus@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "gabriel@gmail.com", "numeros": ["9999999999", "8888888888"]},
]


class TelaAdministrador(CoresTela):

    def __init__(self, page : ft.Page, login_callback):
        super().__init__()
        self.page = page
        self.login_callback = login_callback
        self.conteudo_pagina_principal = ft.Container( content = None, expand=True, alignment=ft.alignment.top_left)


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
            wrap=True,
            spacing=20,
            run_spacing=20,
            expand = True,
            scroll = ft.ScrollMode.AUTO,
            controls=[self.criar_cartao_cliente(c) for c in clientes],
            alignment = ft.alignment.top_left
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
                                d["numero"],
                                d["solicitante"],
                                d["descricao"],
                                d["status"]
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
                            width=float("inf"),
                            border=ft.border.all(1),
                            padding=ft.padding.all(5),
                            margin=ft.margin.only(bottom=5),
                            content=ft.Row([
                                ft.Text("Solicitante:", weight=ft.FontWeight.BOLD),
                                ft.Text(solicitante)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ),
                        ft.Container(
                            width=float("inf"),
                            border=ft.border.all(1),
                            padding=5,
                            margin=ft.margin.only(bottom=5),
                            content=ft.Text(f"Tipo: {descricao}", size=12)
                        ),
                        ft.Row([
                            ft.Text("Status:", weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=menu,
                                bgcolor=self.cor_botao,
                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius=10,
                                alignment=ft.alignment.center
                            )
                        ], alignment=ft.MainAxisAlignment.END)
                    ])
                )
            ])
        )



    def pagina_planos(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Os planos estarão aqui...", size = 20)
        self.page.update()

    def sair(self) -> None:

        alerta_dialogo = None 

        def confirmar_saida(e = None):
            nonlocal alerta_dialogo
            self.page.close(alerta_dialogo)
            self.page.update()
            threading.Timer(0.2, lambda: self.login_callback(self.page)).start()
        
        def cancelar_saida(e = None):
            nonlocal alerta_dialogo
            self.page.close(alerta_dialogo)
            self.page.update()
            threading.Timer(0.2, lambda: self.pagina_principal()).start()

        alerta_dialogo = ft.AlertDialog(
            modal = True, title = ft.Text("Confirme a ação"),
            content = ft.Text("Deseja sair?"),
            actions = [
                ft.TextButton("Sair", on_click = confirmar_saida),
                ft.TextButton("Cancelar", on_click = cancelar_saida)
            ],
            actions_alignment = ft.MainAxisAlignment.END,
        )

        self.page.dialog = alerta_dialogo
        self.page.open(alerta_dialogo)
        self.page.update()