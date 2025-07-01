import flet as ft
from ui.base.SubTela import SubTela
import datetime
from models.plano import Plano
from models.numero import Numero


class PaginaNumeros(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela = tela_admin)


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

        for campo, _ in campos:
            if hasattr(campo, "on_change"):
                original_on_change = campo.on_change

                def combinado(e, original=original_on_change):
                    if original:
                        original(e)  # Mantém o comportamento anterior (ex: validação de float)
                    verificar_campos(e)  # Faz a validação dos campos preenchidos

                campo.on_change = combinado

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

        row_desc = None
        if descricao == None:
            row_desc = ft.Text(descricao)
        else:
            row_desc = ft.Divider(thickness=1)

        
        # Cria a caixa de diálogo padrão
        dialogo = ft.AlertDialog(
            modal=True, title=ft.Text(titulo, weight=ft.FontWeight.BOLD), bgcolor=self.tela.cor_dialogo,
            content=ft.Container(
                width=420, height=altura, padding=10,
                content=ft.Column([
                    row_desc,
                    ft.Container(
                        padding=ft.padding.only(top=2), content=ft.Column(campos_layout + [mensagem_erro], spacing=8)
                    )
                ], spacing=10)
            ),
            actions=[solicitar, ft.TextButton("Cancelar", on_click=fechar_dialogo)]
        )
        self.tela.page.dialog = dialogo
        self.tela.page.open(dialogo)
        self.tela.page.update()

    
    def pagina_meus_numeros(self) -> None:
        
        self.numeros_usuario = [num.numero for num in self.tela.bd.numeros.buscar_por_cpf(self.tela.usuario.cpf)]
        container = self.tela.numeros_expandiveis_ref.current
        coluna = self.tela.numeros_lista_ref.current

        if container.height == 0:
            # Expandir
            coluna.controls = [
                ft.TextButton(
                    text=self.tela.formatarNumero(num),
                    icon=ft.Icons.CHEVRON_RIGHT,
                    on_click= self.pagina_numero,
                    data = num,
                    width=200, height=40,
                    style = ft.ButtonStyle(
                        padding = 2, alignment = ft.alignment.center_left, shape = ft.RoundedRectangleBorder(radius=4),
                        bgcolor= ft.Colors.with_opacity(0.04, ft.Colors.ON_SURFACE)
                    )
                )
                for num in self.tela.numeros_usuario
            ]
            container.height = len(self.tela.numeros_usuario) * 45 + 10
        else:
            # Colapsar
            container.height = 0

        container.update()
    
    
    def pagina_numero(self, e : ft.ControlEvent = None):

        # Obtém o número e suas informações
        numero = self.tela.bd.numeros.obter_numero(e.control.data)
        plano = None

        status = ft.Text()
        nome_plano = ft.Text()

        if numero.assinatura is None:
            plano = None
            status.value = "Status: Sem assinatura"
        else:
            plano = self.tela.bd.assinaturas.obter_plano(numero.assinatura)
            if numero.assinatura.ativa:
                status.value = 'Status: Ativa'
            else:
                status.value = 'Status: Suspenso (inativo)'

        ver_detalhes_plano = self.tela.criar_botao("Ver detalhes", cor=False, funcao= lambda e:self.detalhes_plano(plano=plano))
        if plano == None:
            nome_plano.value = "---"
            ver_detalhes_plano.disabled = True
        else:
            nome_plano.value = plano.nome
            ver_detalhes_plano.disabled = False

        
        def card_titulo(texto : str = '', icone : ft.Icon = None) -> ft.Row:
            return ft.Row([ft.Icon(icone, size = 24), ft.Text(texto, size = 18, weight = ft.FontWeight.BOLD)])

        def linha_info(texto : str = '', info : str = '') -> ft.Row:
            return(ft.Row([ft.Text(texto), ft.Text(info, size=14, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

        def barra_progresso(progresso_percentual : float = 0.0) -> ft.ProgressBar:
            return(ft.ProgressBar(value=progresso_percentual/100, 
                    height=10, color=self.tela.cor_barra_progresso, bgcolor=self.tela.cor_cartao_2, width=float('inf')))
        
        def botao_lateral( botao : ft.ElevatedButton = None ) -> ft.Row:
            return ft.Row([botao], alignment=ft.MainAxisAlignment.END)
        
        def formatar_data_assinatura(numero : Numero) -> str:
            if numero.assinatura and numero.assinatura.data_assinatura:
                return numero.assinatura.data_assinatura.strftime('%d/%m/%Y')
            return "Sem assinatura"

        cabecalho = ft.Container(content=ft.Row([
            ft.Column([
                ft.Text(self.tela.formatarNumero(numero.numero), size=22, weight=ft.FontWeight.BOLD),
                ft.Row([ ft.Row(spacing=5, controls=[ft.Text("Plano: ", weight=ft.FontWeight.BOLD, size=16), ft.Text(nome_plano.value, size=16)]),
                        ver_detalhes_plano], spacing = 10),
                ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH),
                        ft.Text(f"Ativo desde: {formatar_data_assinatura(numero)}")], spacing = 5),
                ft.Row([ft.Icon(ft.Icons.DONE), status], spacing = 5),
                ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY),ft.Text("Próxima fatura: R$ 45,90 - Vence: XX/XX/2025")], spacing = 5),
                ],spacing = 10, expand = True, alignment=ft.alignment.top_left),
            ft.Container(expand=False, alignment=ft.alignment.top_right , content=
                         ft.Column([
                            botao_lateral(self.tela.criar_botao("Cancelar número", ft.Icons.CANCEL_OUTLINED, funcao=self.cancelar_numero)),
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
                ft.Row([self.tela.criar_botao("Comprar pacote extra", ft.Icons.ADD, funcao=self.comprar_dados),
                        self.tela.criar_botao("Ver consumo", ft.Icons.LIST_ALT, funcao= lambda e: self.consumo_dados(numero=numero))],
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
                ft.Row([self.tela.criar_botao("Adicionar minutos", ft.Icons.ADD, funcao = lambda e:self.adicionar_minutos(plano=plano)),
                        self.tela.criar_botao("Ver ligações", ft.Icons.LIST_ALT, funcao=self.ver_ligacoes)
                        ], alignment=ft.MainAxisAlignment.START, spacing = 10),
            ])
        )
        mensagens = ft.Container(
            padding = 15, border = ft.border.all(2), border_radius=10,
            content=ft.Column([
                card_titulo("MENSAGENS", ft.Icons.MESSAGE),
                ft.Text(f"{40} de 100 mensagens utilizados ({60} disponíveis)"),
                linha_info("Renova em", "11/07/2025"),
                barra_progresso(40),
                ft.Row([self.tela.criar_botao("Comprar pacote de mensagens", ft.Icons.ADD, funcao=lambda e:self.comprar_mensagens(plano=plano)),
                        self.tela.criar_botao("Ver histórico", ft.Icons.LIST_ALT, funcao=self.ver_mensagens)],
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
                ft.Row([self.tela.criar_botao("Fazer recarga", ft.Icons.ADD, funcao=self.recarga),
                        self.tela.criar_botao("Ver histórico", ft.Icons.LIST_ALT, funcao=self.historico_saldos)],
                       alignment=ft.MainAxisAlignment.START, spacing = 10),
            ])
        )
        self.tela.atualizar_pagina(
            ft.Column(
                [cabecalho, ft.Divider(thickness=2),
                ft.Row([
                    ft.Column([internet, mensagens], expand = True, alignment = ft.MainAxisAlignment.START, width = 450), 
                    ft.Column([minutos, saldos], expand = True, alignment = ft.MainAxisAlignment.START, width = 450)
                ], expand = True
                , alignment = ft.alignment.top_left)], spacing=20, scroll=ft.ScrollMode.AUTO
            )
        )


    def detalhes_plano(self, e = None, plano : Plano = None) -> None:

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
            modal = True, title = ft.Text(plano.nome, weight=ft.FontWeight.BOLD),
            content=ft.Container(width=350, height=160, padding = 10, content = ft.Column([
                linha('Valor', 'R$ ' + f'{plano.preco}'),
                linha('Dados de Internet', f'{plano.dados_mb}' + ' MB'),
                linha('Máximo de Ligações', f'{plano.maximo_ligacao}'),
                linha('Minutos máx. ligação', f'{plano.minutos_max_ligacao}'),
                linha('Máximo de Mensagens', f'{plano.maximo_mensagens}')
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

    
    def adicionar_minutos(self, e : ft.ControlEvent = None, plano : Plano = None) -> None:
        
        senha = self.tela.textField(tamanho=130, texto=True)
        confirmar_senha = self.tela.textField(tamanho=130, texto=True)
        senha.password = True
        confirmar_senha.password = True
        msg_erro = ft.Text('Senha incorreta.', color = ft.Colors.RED, visible=False)

        saldo = 10.00
        saldo_atual = ft.Text(f"R$ {saldo}")
        
        texto_info = ft.Text("")
        valor = ft.Text('R$ 0.00')
        slider = ft.Slider(min=10, max=100, divisions=9, label='{value}', width=160)

        def slider_change(e : ft.ControlEvent = None) -> None:
            nonlocal texto_info
            nonlocal valor
            texto_info.value = f"{e.control.value} minutos"
            valor.value = f"R$ {e.control.value * plano.pacote_minutos_unitario}"
            self.tela.page.update()

        def confirmar(e = None) -> None:
            nonlocal senha
            nonlocal confirmar_senha
            if (self.tela.bd.usuarios.login(self.tela.usuario.email, senha.value)) and confirmar_senha.value == senha.value:
                self.tela.page.close(self.tela.page.dialog)
                self.tela.page.update()
            else:
                msg_erro.visible = True
                self.tela.page.update()

        slider.on_change_end = slider_change

        self.criar_dialogo(
            titulo = "Comprar pacote de minutos extra", descricao=None,
            campos=[(saldo_atual, 'Saldo atual'), (ft.Text(f'R$ {plano.pacote_minutos_unitario}'), 'Preço unitário'),
                    (slider, "Selecione os minutos extra"), (texto_info, "Pacote"), (valor, "Valor"),
                    (senha, "Digite sua senha"), (confirmar_senha, "Confirme sua senha"), (msg_erro,'')],
            acao_confirmar=confirmar,
            altura=370
        )


    def comprar_mensagens(self, e : ft.ControlEvent = None, plano : Plano = None) -> None:
        
        senha = self.tela.textField(tamanho=130, texto=True)
        confirmar_senha = self.tela.textField(tamanho=130, texto=True)
        senha.password = True
        confirmar_senha.password = True
        msg_erro = ft.Text('Senha inválida.', color = ft.Colors.RED, visible=False)
        saldo = 10.00
        saldo_atual = ft.Text(f"R$ {saldo}")

        texto_info = ft.Text("")
        valor = ft.Text('R$ 0.00')
        slider = ft.Slider(min=10, max=100, divisions=9, label='{value}', width=160)

        def slider_change(e : ft.ControlEvent = None) -> None:
            nonlocal texto_info
            nonlocal valor
            texto_info.value = f"{e.control.value} mensagens"
            valor.value = f"R$ {e.control.value * plano.pacote_mensagem_unitario}"
            self.tela.page.update()

        def confirmar(e : ft.ControlEvent = None) -> None:
            nonlocal senha
            nonlocal confirmar_senha
            if (self.tela.bd.usuarios.login(self.tela.usuario.email, senha.value)) and confirmar_senha.value == senha.value:
                self.tela.page.close(self.tela.page.dialog)
                self.tela.page.update()
            else:
                msg_erro.visible = True
                self.tela.page.update()

        slider.on_change_end = slider_change

        self.criar_dialogo(
            titulo = "Comprar pacote de mensagens",
            descricao = None,
            campos=[(saldo_atual, 'Saldo atual'), (ft.Text(f'R$ {plano.pacote_mensagem_unitario}'), 'Preço unitário'),
                    (slider, "Selecione o pacote de mensagens"), (texto_info, "Pacote"), (valor, "Valor"),
                    (senha, "Digite sua senha"), (confirmar_senha, "Confirme sua senha"), (msg_erro,'')],
            acao_confirmar=confirmar,
            altura=350
        )


    def recarga(self, e : ft.ControlEvent = None) -> None:
        
        senha = self.tela.textField(tamanho=130, texto=True)
        confirmar_senha = self.tela.textField(tamanho=130, texto=True)
        senha.password = True
        confirmar_senha.password = True
        msg_erro = ft.Text('Senha inválida.', color = ft.Colors.RED, visible=False)
        saldo = 10.00
        saldo_atual = ft.Text(f"R$ {saldo}")

        adicionar_saldo = self.tela.textField(tamanho=130, flutuante=True, prefixo='R$ ')

        def confirmar(e : ft.ControlEvent = None) -> None:
            nonlocal senha
            nonlocal confirmar_senha
            if (self.tela.bd.usuarios.login(self.tela.usuario.email, senha.value)) and confirmar_senha.value == senha.value:
                self.tela.page.close(self.tela.page.dialog)
                self.tela.page.update()
            else:
                msg_erro.visible = True
                self.tela.page.update()

        self.criar_dialogo(
            titulo = "Adicionar saldo ao número (recarga)",
            descricao = "Usando o saldo do número, você pode comprar minutos de ligação adicionais, mensagens adicionais ou pagar suas faturas.",
            campos=[(saldo_atual, 'Saldo atual'), (adicionar_saldo,'Valor de recarga'), (senha, 'Digite sua senha'), (confirmar_senha, 'Confirme sua senha'), (msg_erro,'')],
            acao_confirmar=confirmar,
            altura=200
        )


    def comprar_dados(self, e : ft.ControlEvent = None) -> None:
        
        senha = self.tela.textField(tamanho=130, texto=True)
        confirmar_senha = self.tela.textField(tamanho=130, texto=True)
        senha.password = True
        confirmar_senha.password = True
        msg_erro = ft.Text('Senha inválida.', color = ft.Colors.RED, visible=False)
        texto_info = ft.Text("")
        valor = ft.Text('R$ 0.00')

        saldo = 10.00
        saldo_atual = ft.Text(f"R$ {saldo}")

        # Selecionar quanto de dados adicionar (MB)
        slider = ft.Slider(min=500, max=2000, divisions=5, label='{value}', width=160)

        def slider_change(e : ft.ControlEvent = None) -> None:
            nonlocal texto_info
            nonlocal valor
            texto_info.value = f"{e.control.value} MB"
            valor.value = f"R$ {e.control.value * 0.05}"
            self.tela.page.update()

        def confirmar(e : ft.ControlEvent = None) -> None:
            nonlocal senha
            nonlocal confirmar_senha
            if (self.tela.bd.usuarios.login(self.tela.usuario.email, senha.value)) and confirmar_senha.value == senha.value:
                self.tela.page.close(self.tela.page.dialog)
                self.tela.page.update()
            else:
                msg_erro.visible = True
                self.tela.page.update()

        slider.on_change_end = slider_change

        self.criar_dialogo(
            titulo = "Comprar pacote de mensagens",
            descricao = "Ao comprar o pacote de dados de internet, em até 2 minutos eles estarão disponíveis para você aproveitar como quiser!",
            campos=[(saldo_atual, 'Saldo atual'), (slider, "Selecione os dados extra"), (texto_info, "Dados a adicionar"), (valor, "Valor"),
                    (senha, "Digite sua senha"), (confirmar_senha, "Confirme sua senha"), (msg_erro,'')],
            acao_confirmar=confirmar,
            altura=350
        )


    def historico_saldos(self, e : ft.ControlEvent = None) -> None:

        def criar_linha(dados : list[str] = None) -> ft.DataRow:
            return ft.DataRow(cells=[ft.DataCell(ft.Text(dado)) for dado in dados])
        
        cabecalho = ft.Container(content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY), ft.Text("Histórico de transações", weight=ft.FontWeight.BOLD, size = 22)], spacing=15),
            ft.Row([ft.Text("Número: ", weight=ft.FontWeight.BOLD, size=20), ft.Text("(31) XXXXX-XXXX", size=20)], spacing=5)
        ]))
        
        transacoes = ft.Container( expand=True, padding=ft.padding.all(20), border=ft.border.all(1), border_radius=8, content=
            ft.Column(spacing = 20, controls=[
                ft.Row([ft.Icon(ft.Icons.PAYMENTS), ft.Text("Histórico de transações", size=18, weight=ft.FontWeight.BOLD)], spacing = 15),
                ft.DataTable(
                    expand= True, width=750,
                    columns=[ft.DataColumn(ft.Text("Data/Hora", weight=ft.FontWeight.BOLD)),
                             ft.DataColumn(ft.Text("Tipo de Transação", weight=ft.FontWeight.BOLD)),
                             ft.DataColumn(ft.Text("Valor", weight=ft.FontWeight.BOLD)),
                             ft.DataColumn(ft.Text("Descrição", weight=ft.FontWeight.BOLD)) ],
                    rows=[
                        criar_linha(['20/06/2025 10:35', 'Recarga', 'R$ 20.00', 'Recarga via app']),
                        criar_linha(['15/05/2025 10:35', 'Recarga', 'R$ 15.00', 'Recarga via app']) ]
                )
            ])
        )

        self.tela.atualizar_pagina(ft.Column([
            cabecalho, ft.Divider(thickness=2),transacoes
        ], spacing = 20))
    
    
    def consumo_dados(self, e : ft.ControlEvent = None, numero : Numero = None) -> None:
        
        def criar_linha(dados : list[str] = None) -> ft.DataRow:
            return ft.DataRow(
                cells=[ft.DataCell(ft.Text(dado)) for dado in dados]
            )
        
        cabecalho = ft.Container(content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.BAR_CHART), ft.Text("Detalhe de consumo de Internet", weight=ft.FontWeight.BOLD, size = 22)], spacing=15),
            ft.Row([ft.Text("Número: ", weight=ft.FontWeight.BOLD, size=20), ft.Text(self.tela.formatarNumero(numero.numero), size=20)], spacing=5)
        ]))

        periodo = ft.DatePicker(first_date=datetime.datetime(year=2000, month=10, day=1), last_date=datetime.datetime(year=2025, month=10, day=1))

        botao_filtro = ft.OutlinedButton('Selecionar período',
                                         icon=ft.Icons.CALENDAR_MONTH,
                                         on_click = lambda e : self.tela.page.open(periodo))

        consumo_diario = ft.Container(expand=True, padding=ft.padding.all(20), border=ft.border.all(1), border_radius=8 ,content=
            ft.Column(spacing = 20, controls=[
                ft.Row([ft.Icon(ft.Icons.TODAY), ft.Text("Consumo diário", size=18, weight=ft.FontWeight.BOLD)], spacing = 15),
                ft.DataTable(
                    expand= True, width=600,
                    columns=[ft.DataColumn(ft.Text("Data", weight=ft.FontWeight.BOLD)),
                             ft.DataColumn(ft.Text("MB consumidos", weight=ft.FontWeight.BOLD)),
                             ft.DataColumn(ft.Text("Tipo de uso", weight=ft.FontWeight.BOLD))],
                    rows=[
                        criar_linha(['01/06/2025', '150 MB', 'Streaming']),
                        criar_linha(['02/06/2025', '70 MB', 'Navegação'])]
                )
            ])
        )

        resumo = ft.Container(expand=True, padding=ft.padding.all(20), border=ft.border.all(1), border_radius=8, content = 
            ft.Column(spacing = 20, controls= [
                ft.Row([ft.Icon(ft.Icons.QUERY_STATS), ft.Text("Estatísticas", size=18, weight=ft.FontWeight.BOLD)], spacing = 15),
                ft.DataTable(
                    expand= True,width=600,
                    columns=[ft.DataColumn(ft.Text("Métrica", weight=ft.FontWeight.BOLD)), ft.DataColumn(ft.Text("Valor", weight=ft.FontWeight.BOLD))],
                    rows=[
                        criar_linha(['Total de dados consumidos', '3.2 GB']),
                        criar_linha(['Média diária de consumo', '120 MB/dia']),
                        criar_linha(['Dia de maior consumo', '03/06/2025 (300 MB)']),
                        criar_linha(['Porcentagem do pacote utilizado', '64 %'])]
                )
            ])
        )

        self.tela.atualizar_pagina(ft.Column([
            cabecalho, ft.Divider(thickness=2), ft.Column([botao_filtro, consumo_diario, resumo], spacing=35)
        ]))

    
    def ver_mensagens(self, e : ft.ControlEvent = None) -> None:

        cabecalho = ft.Column(spacing = 5, controls=[
            ft.Row([ft.Icon(ft.Icons.MESSAGE), ft.Text("Mensagens de (31) XXXXX-XXXX", weight=ft.FontWeight.BOLD, size=22)], spacing = 15),
            ft.Row([ft.Text("Número de mensagens: ", weight=ft.FontWeight.BOLD), ft.Text('1')], spacing = 5)
        ])

        filtro = self.tela.dropdown(listaOpcoes=['Mais antigo', 'Mais recente'], tamanho=150)

        filtros = ft.Row(spacing = 25, controls=[
            ft.Row(spacing = 25, controls=[
                ft.Text("Ordem de apresentação", weight=ft.FontWeight.BOLD), filtro
            ])
        ])

        mensagens = ft.Container(border=ft.border.all(1), expand=True, content=ft.DataTable(
            columns = [
                ft.DataColumn(ft.Text("Data/Hora")), ft.DataColumn(ft.Text("Destinatário")),
                ft.DataColumn(ft.Text("Texto da Mensagem")), ft.DataColumn(ft.Text(""))
            ], 
            rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("XX/XX/2025 15:22")),
                    ft.DataCell(ft.Text("(31) XXXXX-XXXX")),
                    ft.DataCell(ft.Text(f"'Oi, tudo bem?'")),
                    ft.DataCell(ft.OutlinedButton(text='Ver mensagem', icon=ft.Icons.MESSAGE))
                ]),
            ]
        ))

        self.tela.atualizar_pagina(ft.Column([cabecalho, ft.Divider(thickness=2), ft.Column(spacing=35, controls= [filtros, mensagens])]))
    
    
    def ver_ligacoes(self, e : ft.ControlEvent = None) -> None:

        cabecalho = ft.Column(spacing = 5, controls=[
            ft.Row([ft.Icon(ft.Icons.MESSAGE), ft.Text("Mensagens de (31) XXXXX-XXXX", weight=ft.FontWeight.BOLD, size=22)], spacing = 15),
            ft.Row([ft.Text("Número de mensagens: ", weight=ft.FontWeight.BOLD), ft.Text('1')], spacing = 5)
        ])

        filtro = self.tela.dropdown(listaOpcoes=['Mais antigo', 'Mais recente'], tamanho=150)

        filtros = ft.Row(spacing = 25, controls=[
            ft.Row(spacing = 25, controls=[
                ft.Text("Ordem de apresentação", weight=ft.FontWeight.BOLD), filtro
            ])
        ])

        ligacoes = ft.Container(border=ft.border.all(1), expand=True, content=ft.DataTable(
            columns = [
                ft.DataColumn(ft.Text("Data/Hora de início")), ft.DataColumn(ft.Text("Data/Hora de término")),
                ft.DataColumn(ft.Text("Destinatário")), ft.DataColumn(ft.Text("Duração"))
            ], 
            rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("XX/XX/2025 15:22")), ft.DataCell(ft.Text("XX/XX/2025 15:24")),
                    ft.DataCell(ft.Text("(31) XXXXX-XXXX")), ft.DataCell(ft.Text(f"2 min")),
                ]),
            ]
        ))

        self.tela.atualizar_pagina(ft.Column([cabecalho, ft.Divider(thickness=2), ligacoes]))


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