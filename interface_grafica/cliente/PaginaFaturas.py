import flet as ft
from interface_grafica.base.SubTela import SubTela

# FATURAS DO CLIENTE

class PaginaFaturas(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela_admin=tela_admin)


    def pagina_faturas(self) -> None:

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
            label="Escolha um número", options=[ft.dropdown.Option(n) for n in self.tela.numeros_fake],
            on_change = atualizar_fatura, ref=numero_selecionado, width=300,
        )
        mes_dropdown = ft.Dropdown(
            label="Mês de Referência", options = [ft.dropdown.Option(m) for m in meses],
            on_change = atualizar_fatura, ref = mes_selecionado, width=300,
        )

        self.tela.atualizar_pagina(
            ft.Column([
                ft.Text("Faturas", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(thickness=2),
                ft.Row([numero_dropdown, mes_dropdown], spacing=20),
                ft.Container(ref=container_detalhes, padding=10)
                ], spacing=20, scroll=ft.ScrollMode.AUTO
            )
        )