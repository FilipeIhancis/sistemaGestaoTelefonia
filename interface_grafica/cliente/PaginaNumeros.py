import flet as ft
from interface_grafica.base.SubTela import SubTela



class PaginaNumeros(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela_admin=tela_admin)

    
    def pagina_meus_numeros(self) -> None:
        
        container = self.tela.numeros_expandiveis_ref.current
        coluna = self.tela.numeros_lista_ref.current

        if container.height == 0:
            # Expandir
            coluna.controls = [
                ft.TextButton(
                    text=num, icon=ft.Icons.CHEVRON_RIGHT,
                    on_click= self.pagina_numero, width=200, height=40,
                    style = ft.ButtonStyle(
                        padding = 5,
                        alignment = ft.alignment.center_left,
                        shape = ft.RoundedRectangleBorder(radius=4),
                        bgcolor= ft.Colors.with_opacity(0.04, ft.Colors.ON_SURFACE)
                    )
                )
                for num in self.tela.numeros_fake
            ]
            container.height = len(self.tela.numeros_fake) * 45 + 10
        else:
            # Colapsar
            container.height = 0

        container.update()


    def pagina_numero(self, e):
        
        def card_titulo(texto : str = '', icone : ft.Icon = None) -> ft.Row:
            return ft.Row([ft.Icon(icone, size = 24), ft.Text(texto, size = 18, weight = ft.FontWeight.BOLD)])

        def linha_info(texto : str = '', info : str = '') -> ft.Row:
            return(ft.Row([ft.Text(texto), ft.Text(info, size=14, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

        def barra_progresso(progresso_percentual : float = 0.0) -> ft.ProgressBar:
            return(ft.ProgressBar(value=progresso_percentual/100, 
                    height=10, color=self.tela.cor_barra_progresso, bgcolor=self.tela.cor_cartao_2, width=float('inf')))

        cabecalho = ft.Row([
            ft.Column([ ft.Text(e.control.text, size=22, weight=ft.FontWeight.BOLD),
                        ft.Row([ft.Text("Nome do plano", size=16), self.tela.criar_botao("Ver detalhes", cor=False)], spacing = 10),
                        ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH),ft.Text("Ativo desde: XX/XX/2025")], spacing = 5),
                        ft.Row([ft.Icon(ft.Icons.DONE), ft.Text("Status: Ativa")], spacing = 5),
                        ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY),ft.Text("Próxima fatura: R$ 45,90 - Vence: XX/XX/2025")], spacing = 5),
                        ],spacing = 10, expand = True, alignment=ft.alignment.top_left),
            ft.Column([ self.tela.criar_botao("Cancelar número", ft.Icons.CANCEL),
                        self.tela.criar_botao("Transferir número", ft.Icons.COMPARE_ARROWS),
                        self.tela.criar_botao("Mudar assinatura (Plano)")],
                        alignment=ft.alignment.top_right)
        ])
        internet = ft.Container(
            padding = 15, border = ft.border.all(2), border_radius = 10,
            content = ft.Column([
                card_titulo("INTERNET", ft.Icons.WIFI),
                ft.Text(f"{73}% utilizados ({730} MB de {1000} MB)"),
                barra_progresso(73),
                ft.Row([self.tela.criar_botao("Comprar pacote extra", ft.Icons.ADD),
                        self.tela.criar_botao("Ver consumo", ft.Icons.LIST_ALT)],
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
                ft.Row([self.tela.criar_botao("Adicionar minutos", ft.Icons.ADD),
                        self.tela.criar_botao("Ver ligações", ft.Icons.LIST_ALT)],
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
                ft.Row([self.tela.criar_botao("Comprar pacote de mensagens", ft.Icons.ADD),
                        self.tela.criar_botao("Ver histórico", ft.Icons.LIST_ALT)],
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
                ft.Row([self.tela.criar_botao("Fazer recarga", ft.Icons.ADD),
                        self.tela.criar_botao("Ver histórico", ft.Icons.LIST_ALT)],
                       alignment=ft.MainAxisAlignment.START, spacing = 10),
            ])
        )

        self.tela.atualizar_pagina(
            ft.Column(
            [cabecalho, ft.Divider(thickness=2),
             ft.Row([
             ft.Column([internet, mensagens], expand = True, alignment = ft.MainAxisAlignment.START, width = 450), 
             ft.Column([minutos, saldos], expand = True, alignment = ft.MainAxisAlignment.START, width = 450)], expand = True
             , alignment = ft.alignment.top_left)], spacing=20, scroll=ft.ScrollMode.AUTO
            )
        )