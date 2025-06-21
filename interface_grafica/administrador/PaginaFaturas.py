import flet as ft
from interface_grafica.base.SubTela import SubTela

class PaginaFaturas(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)

    def reenviar_fatura(self, e) -> None:
        print("Reenviando fatura clicada")
    
    def ver_detalhes_fatura(self, e) -> None:
        print("Visualizar detalhes da fatura clicada")

    def ver_faturas_cliente(self, e) -> None:

        cabecalho = ft.Container(content = ft.Column([ft.Text("Cliente: João da Silva", size = 22, weight = ft.FontWeight.BOLD),
                                                      ft.Text("CPF: XXX.XXX.XXX-XX", size = 22, weight = ft.FontWeight.BOLD),
                                                      ft.Text("Números ativos: (31) xxxxx-xxxx | (31) yyyyy-yyyy", size = 14)]))

        faturas = ft.Column(
            [self.criar_cartao_fatura(['(31) xxxxxxxxx', 'X/2025', 49.90, 'Em aberto', 'XX/XX/2025', 'YY/YY/2025']),
             self.criar_cartao_fatura(['(31) yyyyyyyyy', 'Z/2025', 39.90, 'Vencida', 'XX/XX/2025', 'YY/YY/2025'])]
        )

        self.tela.atualizar_pagina(ft.Column(controls = [cabecalho, ft.Divider(thickness=2), faturas], scroll = ft.ScrollMode.AUTO))


    def criar_cartao_fatura(self, fatura : list = []) -> ft.Container:

        numero = fatura[0]
        periodo = fatura[1]
        valor = fatura[2]
        status = fatura[3]
        vencimento = fatura[4]
        geracao = fatura[5]

        def botao(texto : str, funcao, icone : ft.Icon):
            return ft.ElevatedButton(text = texto, bgcolor=self.tela.cor_botao, color=ft.Colors.WHITE, on_click = funcao, icon = icone)

        return ft.Container(
            padding = 10, border = ft.border.all(1), border_radius = 6,
            content = ft.Column([
                    ft.Text("FATURA", weight = ft.FontWeight.BOLD, size = 18) ,
                    ft.Row([
                        ft.Column([
                                ft.Text(f"Número associado: ({numero})", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Período: {periodo}"),
                                ft.Text(f"Valor: R$ {valor:.2f}"),
                            ], alignment=ft.MainAxisAlignment.START, spacing=5,),
                        ft.Column([
                                ft.Text(f"Status: {status}"),
                                ft.Text(f"Data de vencimento: {vencimento}"),
                                ft.Text(f"Data de geração: {geracao}"),
                            ], alignment=ft.MainAxisAlignment.START, spacing=5,)
                    ], alignment = ft.MainAxisAlignment.SPACE_BETWEEN, spacing = 20, vertical_alignment=ft.CrossAxisAlignment.START
                    ),
                    ft.Row([botao("Reenviar Cobrança", self.reenviar_fatura, ft.Icons.SEND),
                            botao("Visualizar Detalhes", self.ver_detalhes_fatura, ft.Icons.EXPAND_MORE),
                            botao("Suspender Número", self.suspender_numero, ft.Icons.CANCEL)
                    ], spacing=10, alignment=ft.MainAxisAlignment.START),
                ], spacing = 10,
            )
        )
    
    def suspender_numero(self, e) -> None:
        print("Suspender número da fatura clicada")
