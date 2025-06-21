import flet as ft
from ui.base.SubTela import SubTela

class PaginaSolicitacoes(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela_admin)
        self.__tela = tela_admin

    def pagina_solicitacoes(self) -> None:
        
        # Exemplo de dados
        dados = [
            {"numero": "001", "solicitante": "João", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
            {"numero": "002", "solicitante": "Maria", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
            {"numero": "003", "solicitante": "Pedro", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
            {"numero": "004", "solicitante": "Ana", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
        ]

        self.tela.atualizar_pagina(
            ft.Column(expand = True, scroll = ft.ScrollMode.AUTO, controls = [
                ft.Row(wrap = True, spacing = 20, run_spacing = 20,
                    controls=[
                        self.criar_cartao_solicitacao(d["numero"], d["solicitante"], d["descricao"], d["status"])
                        for d in dados
                    ]
                )
            ]
            )
        )


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
            bgcolor = self.tela.cor_botao
        )
        return ft.Container(
            width=250, border=ft.border.all(1), border_radius=5,
            content=ft.Column([
                # Cabeçalho sem padding lateral
                ft.Container(
                    width=float("inf"), bgcolor=self.tela.cor_cartao_2, padding=ft.padding.all(10),
                    content=ft.Text(f"Solicitação ({numero})", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), alignment=ft.alignment.center
                ),
                # Corpo com padding interno
                ft.Container(
                    padding=10, content=ft.Column([
                        ft.Container(
                            width=float("inf"), border=ft.border.all(1), padding=ft.padding.all(5), margin=ft.margin.only(bottom=5),
                            content=ft.Row([
                                ft.Text("Solicitante:", weight=ft.FontWeight.BOLD),
                                ft.Text(solicitante)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ),
                        ft.Container(
                            width=float("inf"), border=ft.border.all(1), padding=5, margin=ft.margin.only(bottom=5),
                            content=ft.Text(f"Tipo: {descricao}", size=12)
                        ),
                        ft.Row([
                            ft.Text("Status:", weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content = menu, bgcolor = self.tela.cor_botao, padding = ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius = 10, alignment = ft.alignment.center
                            )
                        ], alignment=ft.MainAxisAlignment.END)
                    ])
                )
            ])
        )