import flet as ft
from InterfaceGrafica.TelaUsuario import TelaUsuario

clientes = [
    {"email": "filipe@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666", "5555555555"]},
    {"email": "gaskdjasd@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "akkaka@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "matheus@gmail.com", "numeros": ["9999999999", "8888888888", "7777777777", "6666666666"]},
    {"email": "gabriel@gmail.com", "numeros": ["9999999999", "8888888888"]},
]


class TelaAdministrador(TelaUsuario):

    def __init__(self, page : ft.Page, login_callback):
        super().__init__(page = page, login_callback = login_callback)

    def pagina_principal(self) -> None:
        
        self.page.clean()           # Limpa a tela

        # Lista de botões do menu lateral
        botoes_menu = [("Cadastrar cliente", ft.Icons.GROUP_ADD), ("Clientes", ft.Icons.GROUPS), ("Solicitações", ft.Icons.CHECKLIST),
                       ("Planos", ft.Icons.LIST_ALT), ("---DIVISOR---", None),  ("Sair", ft.Icons.EXIT_TO_APP)]
        

        # Criando os botões do menu
        menu_controls = []

        for texto, icone in botoes_menu:
            if texto == "---DIVISOR---":
                menu_controls.append(ft.Divider(thickness=1, color="gray"))
            else:
                menu_controls.append(
                    ft.TextButton(
                        text = texto, icon = icone, on_click = self.paginas_menu_lateral, width = 200, height = 45,
                        style = ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=4), alignment=ft.alignment.center_left, padding=10)
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
            ft.Row([menu, ft.VerticalDivider(width=1), self.conteudo_pagina], expand=True, alignment=ft.alignment.top_left)
            ],
            expand=True
        )
        # Cria a página:
        self.page.add(layout)
        self.pagina_clientes()


    def paginas_menu_lateral(self, e : ft.ControlEvent) -> None:
        match  e.control.text:
            case 'Cadastrar cliente':   self.pagina_cadastrar_cliente()
            case 'Clientes':            self.pagina_clientes()
            case 'Solicitações':        self.pagina_solicitacoes()
            case 'Planos':              self.pagina_planos()
            case 'Sair':                self.sair()


    def pagina_cadastrar_cliente(self):
        cabecalho = ft.Text("Cadastro de novo cliente", size=22, weight=ft.FontWeight.BOLD)

        cadastrar = self.criar_botao('Cadastrar')
        cadastrar.disabled = True

        def validar(e=None):
            # Só habilita se ambos os campos estiverem preenchidos
            cadastrar.disabled = not (cpf.value.strip() and email.value.strip())
            self.page.update()

        cpf = ft.TextField(width=200, on_change=validar, border_color=ft.Colors.WHITE, focused_border_color=ft.Colors.WHITE)
        email = ft.TextField(width=200, on_change=validar, border_color=ft.Colors.WHITE, focused_border_color=ft.Colors.WHITE)
        senha = ft.Text("senhaRandom")

        campo = ft.Container( border=ft.border.all(1), border_radius=6, padding=10, expand=True, 
            content=ft.Column([
                    ft.Row(
                        [ft.Text('CPF', weight=ft.FontWeight.BOLD), cpf,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [ft.Text('EMAIL', weight=ft.FontWeight.BOLD), email,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [ft.Text('SENHA', weight=ft.FontWeight.BOLD), senha],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [cadastrar, self.criar_botao('Cancelar')],
                        spacing=10, alignment=ft.MainAxisAlignment.END,
                    )
                ], spacing=15, width=500
            )
        )
        self.atualizar_pagina(ft.Column(controls=[cabecalho, ft.Divider(thickness=2), campo], scroll=ft.ScrollMode.AUTO))



    def criar_cartao_cliente(self, cliente):
        return ft.Container(
            bgcolor = self.cor_cartao_3, alignment= ft.alignment.top_left, border_radius = 5, padding = 10, border=ft.border.all(1), width=280,
            content=ft.Column([
                # Topo com ícone e email
                ft.Row([ ft.Icon(ft.Icons.PERSON, size=30), ft.Text(cliente["email"], weight=ft.FontWeight.BOLD) ]),
                ft.Divider(),
                # Área de números com botão editar
                ft.Container( bgcolor = self.cor_cartao_1, border_radius = 10, padding = 10,
                    content = ft.Column([
                        ft.Text("Números", weight=ft.FontWeight.BOLD),
                            *[
                                ft.Row([ ft.Text(numero, expand=True), self.criar_botao('Editar', cor=False, funcao=self.pagina_edicao_numero)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                                for numero in cliente["numeros"]
                            ]
                    ])
                ),
                ft.Container( alignment=ft.alignment.center,  padding=10,
                    content= ft.Row([self.criar_botao('Ver faturas', funcao=self.ver_faturas_cliente),
                                    self.criar_botao('Adicionar número', funcao=self.pagina_adicionar_numero_cliente)],
                                    spacing = 10, alignment=ft.alignment.center)
                )], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
    

    def pagina_clientes(self) -> None:

        cabecalho = ft.Container(content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.PHONE),ft.Text("Clientes cadastrados", size = 22, weight = ft.FontWeight.BOLD)], spacing = 15)
        ]))

        self.atualizar_pagina(
            ft.Column( controls = [ cabecalho, ft.Divider(thickness=2),
                ft.Row( wrap=True, spacing=20, run_spacing=20, expand = True, scroll = ft.ScrollMode.AUTO,
                        controls=[self.criar_cartao_cliente(c) for c in clientes])
                ], scroll = ft.ScrollMode.AUTO
            )
        )


    def pagina_edicao_numero(self, e) -> None:
        
        cliente = "Joao da Silva".upper()
        cpf_cliente = "XXX.XXX.XXX-XX"

        cabecalho = ft.Container(content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.PHONE),ft.Text("Edição de Número: (31) XXXXX-XXXX", size = 22, weight = ft.FontWeight.BOLD)], spacing = 15),
            ft.Row([ft.Icon(ft.Icons.ACCOUNT_CIRCLE), ft.Text(f"Cliente: {cliente} - CPF: {cpf_cliente}", size = 14)], spacing=15)
        ]))

        def on_change_novo_proprieatario(e = None):
            if novo_proprieatorio.value:
                novo_proprieatorio.label = ''
                novo_proprieatorio.update()

        def on_change_novo_plano(e = None):
            if novo_plano.value:
                novo_plano.label=''
                novo_plano.update()

        cpfs = ['XXX.XXX.XXX-XX', 'YYY.YYY.YYY-YY', 'ZZZ.ZZZ.ZZZ-ZZ']
        planos = ['PLANO 1', 'PLANO 2', 'PLANO 3']

        novo_proprieatorio = ft.Dropdown(label="Cpf", options=[ft.dropdown.Option(cpf) for cpf in cpfs], label_style=ft.TextStyle(size=9),
                                        on_change = on_change_novo_proprieatario, enable_search = True, width=180, text_style=ft.TextStyle(size=9))
        novo_plano = ft.Dropdown(label="Plano", options=[ft.dropdown.Option(plano) for plano in planos], label_style=ft.TextStyle(size=9),
                                 on_change = on_change_novo_plano, enable_search = True, width=180, text_style=ft.TextStyle(size=10))
        
        campo2 = ft.Container( border = ft.border.all(1), border_radius = 6, padding = 10, expand=True,
            content=ft.Column([
            ft.Row( [ft.Icon(ft.Icons.MANAGE_ACCOUNTS), ft.Text("Gerenciamento do número", weight=ft.FontWeight.BOLD, size=16)],spacing=10),
            ft.Divider(thickness=2),
            ft.Row(controls=[
                ft.Column(controls = [
                    ft.Text("Trocar Proprietário:"), ft.Text("Trocar Plano:")
                    ], alignment = ft.MainAxisAlignment.START),
                ft.Column(controls = [
                    ft.Container(content=novo_proprieatorio, padding=ft.padding.only(right=10), width=160),
                    ft.Container(content=novo_plano, width=160)
                    ], alignment = ft.MainAxisAlignment.START)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            # Linha dos dois botões no final
            ft.Row( controls=[ self.criar_botao('Suspender número'), self.criar_botao('Cancelar número') ], alignment=ft.alignment.top_left, spacing=6)
        ]))

        campo1 = ft.Container( expand=True, border = ft.border.all(1), border_radius = 6, padding = 10, content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.INFO), ft.Text("Informações Gerais", weight=ft.FontWeight.BOLD, size=16)],spacing=10),
            ft.Divider(thickness=2),
            ft.Row( controls=[
                    # Coluna da esquerda - os labels
                    ft.Column([
                        ft.Text("Número"), ft.Text("Proprietário (CPF)"), ft.Text("Plano associado"), ft.Text("Status"),
                    ], alignment=ft.MainAxisAlignment.START, spacing=8),

                    # Coluna da direita - os valores
                    ft.Column([
                        ft.Text("(31) XXXXX-XXXX"), ft.Text("XXX.XXX.XXX-XX"), ft.Text("Plano X"), ft.Text("Ativo"),
                    ], alignment=ft.MainAxisAlignment.END, spacing=8),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True
            )
        ]))

        salvar = ft.ElevatedButton("Salvar", bgcolor = self.cor_botao, color = ft.Colors.WHITE,
                                        style=ft.ButtonStyle( padding=ft.padding.symmetric(vertical=15, horizontal=15)))
        cancelar = ft.ElevatedButton("Cancelar", bgcolor = self.cor_botao, color = ft.Colors.WHITE,
                                        style=ft.ButtonStyle( padding=ft.padding.symmetric(vertical=15, horizontal=30)))

        self.atualizar_pagina(
            ft.Column(scroll = ft.ScrollMode.AUTO, controls=[
                cabecalho, ft.Divider(thickness=2), ft.Row([campo1, campo2]), ft.Row([salvar, cancelar])]
            )
        )

    def reenviar_fatura(self, e) -> None:
        print("Reenviando fatura clicada")
    
    def ver_detalhes_fatura(self, e) -> None:
        print("Visualizar detalhes da fatura clicada")

    def suspender_numero(self, e) -> None:
        print("Suspender número da fatura clicada")

    def ver_faturas_cliente(self, e) -> None:

        cabecalho = ft.Container(content = ft.Column([ft.Text("Cliente: João da Silva", size = 22, weight = ft.FontWeight.BOLD),
                                                      ft.Text("CPF: XXX.XXX.XXX-XX", size = 22, weight = ft.FontWeight.BOLD),
                                                      ft.Text("Números ativos: (31) xxxxx-xxxx | (31) yyyyy-yyyy", size = 14)]))

        faturas = ft.Column(
            [self.criar_cartao_fatura(['(31) xxxxxxxxx', 'X/2025', 49.90, 'Em aberto', 'XX/XX/2025', 'YY/YY/2025']),
             self.criar_cartao_fatura(['(31) yyyyyyyyy', 'Z/2025', 39.90, 'Vencida', 'XX/XX/2025', 'YY/YY/2025'])]
        )

        self.atualizar_pagina(ft.Column(controls = [cabecalho, ft.Divider(thickness=2), faturas], scroll = ft.ScrollMode.AUTO))


    def criar_cartao_fatura(self, fatura : list = []) -> ft.Container:

        numero = fatura[0]
        periodo = fatura[1]
        valor = fatura[2]
        status = fatura[3]
        vencimento = fatura[4]
        geracao = fatura[5]

        def botao(texto : str, funcao, icone : ft.Icon):
            return ft.ElevatedButton(text = texto, bgcolor=self.cor_botao, color=ft.Colors.WHITE, on_click = funcao, icon = icone)

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


    def pagina_solicitacoes(self) -> None:
        
        # Exemplo de dados
        dados = [
            {"numero": "001", "solicitante": "João", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
            {"numero": "002", "solicitante": "Maria", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
            {"numero": "003", "solicitante": "Pedro", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
            {"numero": "004", "solicitante": "Ana", "descricao": "xxxxxxxxxxxxxxxxxxxx", "status": "Pendente"},
        ]

        self.atualizar_pagina(
            ft.Column(
                expand = True,
                scroll = ft.ScrollMode.AUTO,
                controls = [
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
            bgcolor = self.cor_botao
        )
        return ft.Container(
            width=250, border=ft.border.all(1), border_radius=5,
            content=ft.Column([
                # Cabeçalho sem padding lateral
                ft.Container(
                    width=float("inf"), bgcolor=self.cor_cartao_2, padding=ft.padding.all(10),
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
                                content = menu, bgcolor = self.cor_botao, padding = ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius = 10, alignment = ft.alignment.center
                            )
                        ], alignment=ft.MainAxisAlignment.END)
                    ])
                )
            ])
        )
    

    def pagina_planos(self) -> None:


        cabecalho = ft.Container(content=ft.Row([
            ft.Column([ft.Text("Planos", weight=ft.FontWeight.BOLD, size = 22)], alignment=ft.alignment.top_left),
            ft.Column([self.criar_botao("Adicionar plano", icone=ft.Icons.ADD, funcao = self.pagina_adicionar_plano)], alignment=ft.alignment.top_right)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        
        def editar(e):
            pass
        def excluir(e):
            pass    
        
        dados = [
            {"nome": "PLANO 1", "valor": "29,30", "dados": 64, "recarga": "15", "max_ligacoes": 10, "max_mensagens": 100, "clientes_usuarios": "45"},
            {"nome": "PLANO 2", "valor": "39,30", "dados": 90, "recarga": "15", "max_ligacoes": 15, "max_mensagens": 100, "clientes_usuarios": "25"},
            {"nome": "PLANO 3", "valor": "49,30", "dados": 100, "recarga": "15", "max_ligacoes": 15, "max_mensagens": 150, "clientes_usuarios": "15"}
        ]

        planos = ft.Column(expand = True, controls=[
            ft.Row(wrap=True, spacing=15, run_spacing=10, controls=[
                self.criar_cartao_plano( d["nome"], d["valor"], d["dados"], d["recarga"],
                                        d["max_ligacoes"], d["max_mensagens"], d["clientes_usuarios"],
                                        self.pagina_editar_plano , excluir)
                for d in dados])
            ])

        self.atualizar_pagina( ft.Column( controls=[cabecalho, ft.Divider(thickness=2), planos], scroll=ft.ScrollMode.AUTO) )


    def criar_cartao_plano(self, nome_plano, valor, dados_internet, valor_recarga, max_ligacoes, max_mensagens, clientes_usuarios, on_editar, on_excluir):

        def linha(label, valor):
            return ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text(label, size=14, weight=ft.FontWeight.BOLD), ft.Text(valor, size=14)])
        
        return ft.Container(
            width=300, border=ft.border.all(2), border_radius=8,
            content=ft.Column([
                # Cabeçalho
                ft.Container(
                    bgcolor= self.cor_cartao_2, padding=ft.padding.all(10), alignment=ft.alignment.center, width=float("inf"),
                    content=ft.Text(nome_plano, color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD), border=ft.border.all(1)
                ),
                # Informações
                ft.Container(content = ft.Container( #border=ft.border.all(1),
                    padding = 15, bgcolor=self.cor_cartao_1, border_radius=4,
                    content=ft.Column([
                        linha("VALOR:", f"R$ {valor}"),
                        linha("DADOS DE INTERNET", f"{dados_internet} GB"),
                        linha("VALOR RECARGA:", f"R$ {valor_recarga}"),
                        linha("MÁXIMO DE LIGAÇÕES", str(max_ligacoes)),
                        linha("MÁXIMO DE MENSAGENS", str(max_mensagens)),
                        linha("CLIENTES USUÁRIOS", str(clientes_usuarios)),
                    ])
                )),
                # Botões
                ft.Container(padding=ft.padding.all(5), content=
                    ft.Row([self.criar_botao('Editar', funcao=on_editar), self.criar_botao('Excluir', funcao=on_excluir)],
                            alignment=ft.MainAxisAlignment.CENTER, spacing=5, expand=True)
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
        
        def validar_input(e):
            texto = e.control.value
            novo_texto = ""
            ponto_encontrado = False

            for i, c in enumerate(texto):
                if c.isdigit():
                    novo_texto += c
                elif c == "." and not ponto_encontrado and i != 0:
                    # Permite o primeiro ponto (não no início)
                    novo_texto += c
                    ponto_encontrado = True
            # Se o texto foi modificado, atualiza
            if texto != novo_texto:
                e.control.value = novo_texto
                self.page.update()
            
        # Campos editáveis
        valor = linha_com_borda("VALOR:", ft.TextField(width=130, prefix_text="R$ ", text_size = 11, on_change=validar_input))
        dados_internet = linha_com_borda("DADOS DE INTERNET:", ft.TextField(width=130, suffix_text=" MB", text_size = 11))
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
        self.atualizar_pagina(
            ft.Column(
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
        )

    def pagina_adicionar_plano(self, e) -> None:

        cabecalho = ft.Row([ft.Icon(ft.Icons.LIST_ALT), ft.Text("Novo Plano", size = 22, weight=ft.FontWeight.BOLD)], spacing=10)

        def criar_linha(texto : str, textField : ft.TextField) -> ft.Row:
            return ft.Row(
                [ft.Text(value=texto, weight=ft.FontWeight.BOLD), textField],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )

        nome = self.textField(tamanho=100)
        max_lig = self.textField(tamanho=100, inteiro=True)
        max_msg = self.textField(tamanho=100, inteiro=True)
        dados_internet = self.textField(tamanho=100, inteiro=True)
        valor_mensal = self.textField(tamanho=100, flutuante=True)
        valor_recarga = self.textField(tamanho=100, flutuante=True)
        valor_pacote_msg = self.textField(tamanho=100, flutuante=True)
        valor_pacote_lig = self.textField(tamanho=100, flutuante=True)
        dados_internet.suffix_text = 'MB'
        valor_mensal.prefix_text = 'R$'
        valor_recarga.prefix_text = 'R$'
        valor_pacote_lig.prefix_text = 'R$'
        valor_pacote_msg.prefix_text = 'R$'
        
        dados = ft.Container(padding=15, width=350, expand=True, border=ft.border.all(1), border_radius=8, content= ft.Column([
            ft.Row([ ft.Icon(ft.Icons.INFO), ft.Text('Dados',size=18, weight=ft.FontWeight.BOLD) ], spacing=10),
            ft.Divider(thickness=1),
            criar_linha('Nome', nome),
            criar_linha('Dados de Internet (MB)', dados_internet),
            criar_linha('Máximo de ligações', max_lig),
            criar_linha('Máximo de mensagens', max_msg)
            ])
        )
        valores = ft.Container(padding = 15, width = 400, expand=True, border=ft.border.all(1), border_radius=8, content=ft.Column([
            ft.Row([ ft.Icon(ft.Icons.ATTACH_MONEY), ft.Text('Valores',size=18, weight=ft.FontWeight.BOLD) ], spacing=10),
            ft.Divider(thickness=1),
            criar_linha('Valor mensal', valor_mensal),
            criar_linha('Valor de recarga', valor_recarga),
            criar_linha('Valor pacote de mensagens', valor_pacote_msg),
            criar_linha('Valor pacote de ligações', valor_pacote_lig)
        ]))

        botoes = ft.Row(spacing = 5, controls=[
            self.criar_botao('Criar', funcao=None), self.criar_botao('Cancelar')
        ])

        self.atualizar_pagina(
            ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
            cabecalho, ft.Divider(thickness=2), ft.Row([dados, valores]), botoes
            ])
        )


    def pagina_adicionar_numero_cliente(self) -> None:

        print("Irá adicionar um novo número ao cliente AQUI!")