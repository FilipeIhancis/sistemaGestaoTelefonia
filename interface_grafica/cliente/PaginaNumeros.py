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
        
        def botao_lateral( botao : ft.ElevatedButton = None ) -> ft.Row:
            return ft.Row([botao], alignment=ft.MainAxisAlignment.END)

        cabecalho = ft.Container(content=ft.Row([
            ft.Column([ ft.Text(e.control.text, size=22, weight=ft.FontWeight.BOLD),
                        ft.Row([ft.Text("Nome do plano", size=16), self.tela.criar_botao("Ver detalhes", cor=False, funcao=self.detalhes_plano)], spacing = 10),
                        ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH),ft.Text("Ativo desde: XX/XX/2025")], spacing = 5),
                        ft.Row([ft.Icon(ft.Icons.DONE), ft.Text("Status: Ativa")], spacing = 5),
                        ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY),ft.Text("Próxima fatura: R$ 45,90 - Vence: XX/XX/2025")], spacing = 5),
                        ],spacing = 10, expand = True, alignment=ft.alignment.top_left),
            ft.Container(expand=False, alignment=ft.alignment.top_right , content=
                         ft.Column([ botao_lateral(self.tela.criar_botao("Cancelar número", ft.Icons.CANCEL_OUTLINED, funcao=self.cancelar_numero)),
                        botao_lateral(self.tela.criar_botao("Transferir número", icone=ft.Icons.PERSON, funcao=self.transferir_numero)),
                        botao_lateral(self.tela.criar_botao("Mudar assinatura (Plano)", icone=ft.Icons.CHANGE_CIRCLE_OUTLINED, funcao=self.mudar_assinatura))],
                        alignment=ft.MainAxisAlignment.END, spacing = 5)
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
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

    
    def detalhes_plano(self, e = None):

        info_plano = None 

        def linha(texto1 : str = '', texto2: str = '') -> ft.Row:
            return ft.Row(
                [ft.Text(texto1, weight=ft.FontWeight.BOLD), ft.Text(texto2)],
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            )

        def fechar_info_plano(e = None):
            nonlocal info_plano
            self.tela.page.close(info_plano)
            self.tela.page.update()

        info_plano = ft.AlertDialog(
            modal = True, title = ft.Text("Plano X", weight=ft.FontWeight.BOLD),
            content=ft.Container(width=350, height=160, padding = 10, content = ft.Column([
                linha('Valor', 'R$ ' + '59,90'),
                linha('Dados de Internet', '1000' + ' MB'),
                linha('Valor de recarga', 'R$ ' + '5,20'),
                linha('Máximo de Ligações', '120'),
                linha('Máximo de Mensagens', '150')
            ])),
            actions = [
                ft.TextButton("Sair", on_click = fechar_info_plano)
            ],
            actions_alignment = ft.MainAxisAlignment.END,
            bgcolor=self.tela.cor_dialogo
        )
        self.tela.page.dialog = info_plano
        self.tela.page.open(info_plano)
        self.tela.page.update()


    def criar_dialogo(self, titulo: str, descricao: str, campos: list, acao_confirmar, altura: int = 200) -> None:

        dialogo = None
        solicitar = ft.TextButton("Solicitar", disabled=True)
        mensagem_erro = ft.Text('Senha incorreta! Tente novamente.', color=ft.Colors.RED, visible=False)

        def verificar_campos(e=None):
            solicitar.disabled = not all(campo.value for campo, _ in campos)
            self.tela.page.update()

        def fechar_dialogo(e=None):
            nonlocal dialogo
            self.tela.page.close(dialogo)
            self.tela.page.update()

        # Liga eventos de validação
        for campo, _ in campos:
            campo.on_change = verificar_campos

        # Define o que o botão "Solicitar" vai fazer
        solicitar.on_click = acao_confirmar

        # Layout dos campos
        campos_layout = []
        for campo, label in campos:
            campos_layout.append(
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text(label, weight=ft.FontWeight.BOLD), campo
                ])
            )
        # Cria a caixa de diálogo padrão
        dialogo = ft.AlertDialog(
            modal=True, title=ft.Text(titulo, weight=ft.FontWeight.BOLD), bgcolor=self.tela.cor_dialogo,
            content=ft.Container(
                width=400, height=altura, padding=10,
                content=ft.Column([
                    ft.Text(descricao),
                    ft.Container(
                        padding=ft.padding.only(top=25),
                        content=ft.Column(campos_layout + [mensagem_erro], spacing=8)
                    )
                ], spacing=10)
            ),
            actions=[solicitar, ft.TextButton("Cancelar", on_click=fechar_dialogo)]
        )
        self.tela.page.dialog = dialogo
        self.tela.page.open(dialogo)
        self.tela.page.update()


    def transferir_numero(self, e: ft.ControlEvent) -> None:
        cpf = self.tela.textField(tamanho=100, inteiro=True)
        senha = self.tela.textField(tamanho=100, texto=True)
        senha.password = True
        confirmar_senha = self.tela.textField(tamanho=100,texto=True)
        confirmar_senha.password = True

        def confirmar(e=None):
            print(f"Transferência solicitada para CPF: {cpf.value}, Senha: {senha.value}")
            self.tela.page.close(self.tela.page.dialog)
            self.tela.page.update()

        self.criar_dialogo(
            titulo="Transferência de número",
            descricao="Solicite a transferência do seu número de telefone. Aguarde 2 dias úteis para a conclusão da transferência.",
            campos=[(cpf, "CPF do novo proprietário"), (senha, "Digite sua senha"), (confirmar_senha, "Confirme sua senha")],
            acao_confirmar=confirmar,
            altura=240
        )
    
    
    def cancelar_numero(self, e: ft.ControlEvent = None) -> None:

        senha = self.tela.textField(tamanho=100, texto=True)
        confirmar_senha = self.tela.textField(tamanho=100, texto=True)
        senha.password = True
        confirmar_senha.password = True

        def confirmar(e=None):
            print(f"Cancelamento solicitado com senha: {senha.value} e confirmação: {confirmar_senha.value}")
            self.tela.page.close(self.tela.page.dialog)
            self.tela.page.update()

        self.criar_dialogo(
            titulo="Cancelar número",
            descricao="O número será cancelado permanentemente após análise. Caso tenha alguma fatura em aberto, a solicitação será negada.",
            campos=[(senha, "Digite sua senha"), (confirmar_senha, "Confirme sua senha")],
            acao_confirmar=confirmar,
            altura=240
        )

    
    def mudar_assinatura(self, e : ft.ControlEvent = None) -> None:
        
        senha = self.tela.textField(tamanho=130, texto=True)
        confirmar_senha = self.tela.textField(tamanho=130, texto=True)
        senha.password = True
        confirmar_senha.password = True

        plans = ['Plano 1', 'Plano 2', 'Plano 3', 'Plano 4']
        novo_plano = self.tela.dropdown('Novo plano', [plan for plan in plans], tamanho=130)

        def confirmar(e = None) -> None:
            print("confirmado ok")
            self.tela.page.close(self.tela.page.dialog)
            self.tela.page.update()

        self.criar_dialogo(
            titulo = "Mudar assinatura (plano)",
            descricao = "O plano será alterado após análise. Caso tenha alguma fatura em aberto, a assinatura não será alterada.",
            campos=[(novo_plano, 'Selecione o plano'), (senha, "Digite sua senha"), (confirmar_senha, "Confirme sua senha")],
            acao_confirmar=confirmar,
            altura=280
        )