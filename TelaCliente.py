import flet as ft
import threading


class TelaCliente():

    def __init__(self, page : ft.Page, login_callback):
        self.page = page
        self.login_callback = login_callback
        self.conteudo_pagina_principal = None


    def pagina_principal(self) -> None:
        
        self.page.clean()   # Limpa a tela
        
        # Função para tratar clique nos botões
        def menu_click(e):
            texto = e.control.text
            match  texto:
                case 'Meus Números':        self.meus_numeros()
                case 'Sair':                self.sair()
                case "Minhas Assinaturas":  self.minhas_assinaturas()
                case "Adicionar Número":    self.adicionar_numero()
                case "Transferir Número":   self.transferir_numero()
                case "Faturas":             self.faturas()
                case "Cancelar Número":     self.cancelar_numero()
                case "Ajuda / Suporte":     self.ajuda_suporte()

        # Lista de botões do menu lateral
        botoes_menu = ["Meus Números", "Minhas Assinaturas", "Adicionar Número", "Transferir Número",
                        "Cancelar Número", "Faturas", "Ajuda / Suporte", "---DIVISOR---", "Sair"]
        
        # Lista de ícones do menu lateral
        lista_icones_botoes = [ ft.Icons.PHONE, ft.Icons.LIST, ft.Icons.PLUS_ONE, ft.Icons.ARROW_RIGHT_ALT_ROUNDED,
            ft.Icons.CANCEL, ft.Icons.PAYMENT, ft.Icons.HELP, None, ft.Icons.EXIT_TO_APP]

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
            content = ft.Text("Área do Cliente", size=20, weight = ft.FontWeight.BOLD, color = "white"),
            padding = 20, alignment = ft.alignment.center,
        )

        # Irá armazenar o conteúdo da página
        self.conteudo_pagina_principal = ft.Container( content = None, expand=True, alignment=ft.alignment.center)

        # Layout principal
        layout = ft.Column([cabecalho, ft.Row([menu, ft.VerticalDivider(width=1), self.conteudo_pagina_principal], expand=True)], expand=True )
        
        # Cria a página:
        self.page.add(layout)

    def meus_numeros(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Números aqui!", size = 20)
        self.page.update()

    def minhas_assinaturas(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Assinaturas!", size = 20)
        self.page.update()

    def adicionar_numero(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Vamos adicionar um novo número.", size = 20)
        self.page.update()
    
    def transferir_numero(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Transferência de números.", size = 20)
        self.page.update()

    def faturas(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Aqui estarão as faturas", size = 20)
        self.page.update()

    def ajuda_suporte(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Ajuda do suporte.....", size = 20)
        self.page.update()

    def cancelar_numero(self) -> None:
        self.conteudo_pagina_principal.content = ft.Text("Cancelando número!", size = 20)
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