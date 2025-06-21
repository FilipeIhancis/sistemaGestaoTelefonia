import flet as ft
from interface_grafica.base.SubTela import SubTela


class PaginaAdicionarNumero(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)


    def pagina_adicionar_numero(self) -> None:

        taxa_solicitacao = 5.0

        cabecalho = ft.Text("Adicionar novo número", size=22, weight=ft.FontWeight.BOLD)

        plano_selecionado = ft.Text("")
        recarga_valor = ft.Text("")

        # Radio group de recarga
        recarga_group = ft.RadioGroup(
            content = ft.Row([
                ft.Radio(value="10", label="R$ 10,00"), ft.Radio(value="20", label="R$ 20,00"),
                ft.Radio(value="30", label="R$ 30,00"), ft.Radio(value="40", label="R$ 40,00"),])
        )

        recarga_group.value = 0

        def selecionar_plano(e : ft.ControlEvent = None) -> None:

            for plano in self.tela.planos_fake:
                plano.border = ft.border.all(1)
            
            # Botão selecionado recebe destaque
            e.control.border = ft.border.all(2, ft.Colors.YELLOW_300)
            e.control.bgcolor = ft.Colors.with_opacity(0.1, self.tela.cor_cartao_1)
            plano_selecionado.value = f"Plano selecionado: {e.control.data}"
            self.tela.page.update()

        def solicitar_numero(e):
            valor_recarga = recarga_group.value
            plano = plano_selecionado.value
            recarga_valor.value = f"Recarga escolhida: R$ {valor_recarga}, {plano}"
            self.tela.page.update()

        # PLANOS FAKE
        plano1 = self.criar_cartao_plano('Plano 1', 1000, 100,50,39.90,30)
        plano2 = self.criar_cartao_plano('Plano 2', 2000, 120,50,49.90,30)
        plano3 = self.criar_cartao_plano('Plano 3', 3500, 150,70,69.90,30)

        plano1.on_click = selecionar_plano
        plano2.on_click = selecionar_plano
        plano3.on_click = selecionar_plano

        self.tela.planos_fake = [plano1, plano2, plano3]

        self.tela.atualizar_pagina( ft.Column([
            cabecalho, ft.Divider(thickness=2),
            ft.Container( content=ft.Column([
                    ft.Text("Escolha seu plano", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([plan for plan in self.tela.planos_fake], alignment=ft.MainAxisAlignment.START),
                ]),
                padding=20, border=ft.border.all(1), border_radius=10, margin=10
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Recarga inicial", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([ ft.Text("Valor: "), recarga_group ]),
                    ft.Row([ft.Text("Taxa de solicitação: ", weight=ft.FontWeight.BOLD), ft.Text(f"R$ {str(taxa_solicitacao)}")], spacing=5),
                    ft.Row([ft.Text("Total a pagar: ", weight=ft.FontWeight.BOLD), ft.Text(f"R$ {float(recarga_group.value) + taxa_solicitacao}")], spacing=5)
                ]),
                padding=10, border=ft.border.all(1), border_radius=10, margin=10
            ),
            ft.Row([self.tela.criar_botao('Solicitar Número', funcao=solicitar_numero),
                    self.tela.criar_botao('Cancelar', funcao=self.tela.pagina_principal())
            ]),
            plano_selecionado,
            recarga_valor],
            scroll=ft.ScrollMode.AUTO
            )
        )

    def criar_cartao_plano(self, nome:str, dados:int, minutos_lig:int, msg:int, valor:float, num_lig:int) -> ft.Container:

        def linha(texto1:str, texto2:str) -> ft.Row:
            return ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text(str(texto1), weight=ft.FontWeight.BOLD), ft.Text(str(texto2))])
        
        return ft.Container(
            border = ft.border.all(1), border_radius = 10, width=300, padding = 8, tooltip="Clique para selecionar", data = nome,
            content = ft.Column(
                [ft.Container(padding = 10, bgcolor=self.tela.cor_cartao_2, width=float('inf'), alignment=ft.alignment.center,
                              content=ft.Row([ft.Text(nome, weight=ft.FontWeight.BOLD, size=17)], alignment=ft.MainAxisAlignment.CENTER)),
                ft.Container(padding = ft.padding.only(left=20,right=20,bottom=20,top=5), content=
                            ft.Column([ linha('Dados de Internet', str(dados)+' MB'),
                            linha('Máximo de ligações', str(num_lig)),
                            linha('Minutos de ligação', str(minutos_lig)),
                            linha('Máximo de mensagens', str(msg)),
                            linha('Valor Mensal', 'R$ ' + str(valor))],
                            spacing = 10)
                )]
            )
        )