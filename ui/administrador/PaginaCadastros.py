import flet as ft
from ui.base.SubTela import SubTela
from models.usuario import Usuario
from datetime import datetime
from models.plano import Plano
from models.usuario import Usuario
from models.numero import Numero
from models.assinatura import Assinatura


class PaginaCadastro(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)


    def cadastrar_cliente(self, e : ft.ControlEvent = None):

        cpf = self.tela.textField(tamanho=200, inteiro=True)
        nome = self.tela.textField(tamanho=200, texto=True)
        email = self.tela.textField(tamanho=200, texto=True)
        senha = ft.Text("senhaRandom")
        mensagem_erro = ft.Text("Dados inválidos. Verifique se o CPF já possui cadastro no sistema.", color=ft.Colors.RED, visible=False)

        cadastrar = self.tela.criar_botao('Cadastrar')
        cadastrar.disabled = True

        def adicionar(e : ft.ControlEvent = None) -> None:
            try:
                cliente = Usuario(nome.value, cpf.value, email.value, senha.value, datetime.now(), 'CLIENTE')
                if (self.tela.bd.usuarios.adicionar_cliente(usuario = cliente)):
                    mensagem_erro.visible = False
                    self.tela.page.update()
                    self.tela.page.open(
                        ft.AlertDialog(
                            title = ft.Text("Cliente adicionado com sucesso"),
                            alignment=ft.alignment.center,
                            bgcolor = self.tela.cor_dialogo
                        )
                    )
                else:
                    mensagem_erro.visible = True
                    self.tela.page.update()

            except ValueError:
                mensagem_erro.visible = True
                self.tela.page.update()

        def validar(e : ft.ControlEvent = None) -> None:
            cadastrar.disabled = not (cpf.value.strip() and email.value.strip())
            self.tela.page.update()

        cadastrar.on_click = adicionar
        cpf.on_change = validar
        email.on_change = validar
        nome.on_change = validar

        cabecalho = ft.Text("Cadastro de novo cliente", size=22, weight=ft.FontWeight.BOLD)

        campo = ft.Container( border=ft.border.all(1), border_radius=6, padding=ft.padding.all(25), expand=True, 
            content=ft.Column([
                    ft.Row(
                        [ft.Text('CPF CLIENTE', weight=ft.FontWeight.BOLD), cpf,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [ft.Text('NOME CLIENTE', weight=ft.FontWeight.BOLD), nome,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [ft.Text('EMAIL', weight=ft.FontWeight.BOLD), email,],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [ft.Text('SENHA (RANDÔMICA)', weight=ft.FontWeight.BOLD), senha],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    mensagem_erro,
                    ft.Row( [cadastrar], spacing=10, alignment=ft.MainAxisAlignment.END )
                ], spacing=15, width=500
            )
        )
        self.tela.atualizar_pagina(ft.Column(controls=[cabecalho, ft.Divider(thickness=2), campo], scroll=ft.ScrollMode.AUTO))


    def cadastrar_plano(self, e : ft.ControlEvent) -> None:

        cabecalho = ft.Row([ft.Icon(ft.Icons.LIST_ALT), ft.Text("Novo Plano", size = 22, weight=ft.FontWeight.BOLD)], spacing=10)

        def criar_linha(texto : str, textField : ft.TextField) -> ft.Row:
            return ft.Row(
                [ft.Text(value=texto, weight=ft.FontWeight.BOLD), textField],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        
        # Entradas do administrador:
        nome = self.tela.textField(tamanho=100)
        max_lig = self.tela.textField(tamanho=100, inteiro=True)
        max_msg = self.tela.textField(tamanho=100, inteiro=True)
        dados_internet = self.tela.textField(tamanho=100, inteiro=True)
        minutos_max = self.tela.textField(tamanho = 100, inteiro=True)
        valor_mensal = self.tela.textField(tamanho=100, flutuante=True)
        valor_pacote_msg = self.tela.textField(tamanho=100, flutuante=True)
        valor_pacote_lig = self.tela.textField(tamanho=100, flutuante=True)

        botao_criar_plano = self.tela.criar_botao('Criar Plano')
        botao_criar_plano.disabled = True

        dados_internet.suffix_text = 'MB'
        valor_mensal.prefix_text = 'R$ '
        valor_pacote_lig.prefix_text = 'R$ '
        valor_pacote_msg.prefix_text = 'R$ '

        def adicionar(e : ft.ControlEvent = None) -> None:
            
            try:
                plano = Plano(nome.value, int(dados_internet.value), float(valor_mensal.value), int(max_msg.value),
                          int(max_lig.value), int(minutos_max.value), float(valor_pacote_msg.value), float(valor_pacote_lig.value))
            except ValueError:
                self.tela.page.open(ft.AlertDialog(
                    title = ft.Text("Erro nos valores", weight=ft.FontWeight.BOLD),
                    content= ft.Text("Preencha os campos corretamente.")
                ))
            if self.tela.bd.planos.plano_existe(nome.value):
                self.tela.page.open(ft.AlertDialog(
                    title = ft.Row([ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED), ft.Text(f"ERRO", weight=ft.FontWeight.BOLD)], spacing=5),
                    content=ft.Text(f"O plano '{nome.value}' já existe no sistema."),
                    bgcolor=self.tela.cor_dialogo
                ))
                self.tela.page.update()
            else:
                self.tela.bd.planos.adicionar_plano(plano)
                self.tela.page.open(ft.AlertDialog(
                    bgcolor=self.tela.cor_dialogo,
                    title=ft.Text('Plano adicionado', weight=ft.FontWeight.BOLD), 
                    content=ft.Text(f"O plano '{nome.value}' foi adicionado ao sistema com sucesso. Acesse a aba 'Planos' para visualizar.")
                ))
                self.tela.page.update()

        def validar(e : ft.ControlEvent = None) -> None:
            botao_criar_plano.disabled = not (nome.value and max_lig.value and max_msg.value and dados_internet.value and minutos_max.value
                                              and valor_mensal.value and valor_pacote_msg.value and valor_pacote_lig.value)
            self.tela.page.update()

        campos = [nome, max_lig, max_msg, dados_internet, minutos_max, dados_internet, minutos_max, valor_mensal, valor_pacote_lig, valor_pacote_msg]
        for campo in campos:
            val_original = campo.on_change
            def combinado(e, original = val_original):
                if original:
                    original(e)
                validar(e)
            campo.on_change = combinado

        botao_criar_plano.on_click = adicionar
        minutos_max.on_change = validar
        nome.on_change = validar
        max_lig.on_change = validar
        max_msg.on_change = validar
        dados_internet.on_change = validar
        valor_mensal.on_change = validar
        valor_pacote_lig.on_change = validar
        valor_pacote_msg.on_change = validar

        dados = ft.Container(padding=15, width=350, expand=True, border=ft.border.all(1), border_radius=8, content= ft.Column([
            ft.Row([ft.Icon(ft.Icons.INFO), ft.Text('Dados',size=18, weight=ft.FontWeight.BOLD) ], spacing=10),
            ft.Divider(thickness=1),
            criar_linha('Nome', nome),
            criar_linha('Dados de Internet (MB)', dados_internet),
            criar_linha('Máximo de ligações', max_lig),
            criar_linha('Minutos máx. em ligação', minutos_max),
            criar_linha('Máximo de mensagens', max_msg)
            ])
        )
        valores = ft.Container(padding = 15, width = 400, expand=True, border=ft.border.all(1), border_radius=8, content=ft.Column([
            ft.Row([ ft.Icon(ft.Icons.ATTACH_MONEY), ft.Text('Valores',size=18, weight=ft.FontWeight.BOLD) ], spacing=10),
            ft.Divider(thickness=1),
            criar_linha('Valor mensal', valor_mensal),
            criar_linha('Valor pacote de mensagens', valor_pacote_msg),
            criar_linha('Valor pacote de ligações', valor_pacote_lig)
        ]))

        self.tela.atualizar_pagina(
            ft.Column(scroll=ft.ScrollMode.AUTO, controls=[
            cabecalho, ft.Divider(thickness=2), ft.Row([dados, valores]), botao_criar_plano
            ])
        )


    def cadastrar_numero(self, e = None) -> None:

        cliente_escolhido = None
        plano_escolhido = None
        numero_aleatorio = self.tela.gerar_numero_telefone()
        texto_numero = ft.Text(self.tela.formatarNumero(numero_aleatorio))

        cpfs = [cliente.cpf for cliente in self.tela.bd.usuarios.obter_clientes()]
        planos = [plano.nome for plano in self.tela.bd.planos.obter_planos()]

        proprietario = self.tela.dropdown('Escolha um cliente', cpfs)
        plano = self.tela.dropdown('Escolha um plano', planos)
        saldo_inicial = self.tela.textField(prefixo='R$ ', tamanho=150, flutuante=True)
        info = ft.Container(padding=20, border_radius=8, border=ft.border.all(1), expand=True)

        # Função auxiliar para criar linhas de info
        def criar_linha(texto1: str, texto2: str) -> ft.Row:
            return ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[ft.Text(texto1, weight=ft.FontWeight.BOLD), ft.Text(texto2)]
            )

        # Função que atualiza o card de informações
        def atualizar_info() -> None:
            nonlocal info
            linhas = [
                criar_linha('Número', self.tela.formatarNumero(numero_aleatorio)),
                ft.Divider(thickness=1),
                criar_linha('Proprietário', cliente_escolhido.cpf if cliente_escolhido else '----'),
                ft.Divider(thickness=1),
                criar_linha('Plano', plano_escolhido.nome if plano_escolhido else '----'),
                ft.Divider(thickness=1),
                criar_linha('Dados (MB)', str(plano_escolhido.dados_mb) if plano_escolhido else '----'),
                ft.Divider(thickness=1),
                criar_linha('Máximo de ligações', str(plano_escolhido.maximo_ligacao) if plano_escolhido else '----'),
                ft.Divider(thickness=1),
                criar_linha('Máximo de mensagens', str(plano_escolhido.maximo_mensagens) if plano_escolhido else '----')
            ]

            info.content = ft.Column(
                [ft.Container(padding=ft.padding.only(bottom=18),
                            content=ft.Row(spacing=5, controls=[
                                ft.Icon(ft.Icons.INFO),
                                ft.Text("Informações do número", size=18, weight=ft.FontWeight.BOLD)
                            ])
                            )] + linhas,
                spacing=2
            )
            self.tela.page.update()

        # Função que trata mudanças nos dropdowns
        def obter_info(e: ft.ControlEvent = None) -> None:
            nonlocal cliente_escolhido, plano_escolhido
            cliente_escolhido = self.tela.bd.usuarios.buscar_usuario_cpf(cpf=proprietario.value)
            plano_escolhido = self.tela.bd.planos.obter_plano(plano.value)
            atualizar_info()

        # Botão de regenerar número
        def alterar_num(e: ft.ControlEvent = None) -> None:
            nonlocal numero_aleatorio
            numero_aleatorio = self.tela.gerar_numero_telefone()
            texto_numero.value = self.tela.formatarNumero(numero_aleatorio)
            atualizar_info()
            self.tela.page.update()

        proprietario.on_change = obter_info
        plano.on_change = obter_info

        linha_num = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("Número", weight=ft.FontWeight.BOLD),
                ft.Row(spacing=10, controls=[
                    texto_numero, ft.IconButton(icon=ft.Icons.AUTORENEW, on_click=alterar_num)
                ])
            ]
        )

        # Card de configuração de dados
        configDados = ft.Container(
            padding=20, border_radius=8, border=ft.border.all(1), expand=True,
            content=ft.Column([
                ft.Container(
                    padding=ft.padding.only(bottom=8),
                    content=ft.Row(spacing=5, controls=[
                        ft.Icon(ft.Icons.SETTINGS),
                        ft.Text("Configuração de dados", size=18, weight=ft.FontWeight.BOLD)
                    ])
                ),
                linha_num,
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("Proprietário", weight=ft.FontWeight.BOLD), proprietario
                ]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("Plano", weight=ft.FontWeight.BOLD), plano
                ]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text("Saldo inicial", weight=ft.FontWeight.BOLD), saldo_inicial
                ])
            ])
        )

        # Função para salvar o número no banco
        def criar(e: ft.ControlEvent = None) -> None:
            if cliente_escolhido and plano_escolhido and saldo_inicial.value:
                self.tela.bd.numeros.salvar(
                    Numero(
                        numero=numero_aleatorio,
                        cpf_proprieatario=cliente_escolhido.cpf,
                        saldo=float(saldo_inicial.value)
                    )
                )
                self.tela.bd.assinaturas.salvar(
                    Assinatura(plano_escolhido, datetime.now(), True)
                )
                self.tela.page.open(ft.AlertDialog(
                    title=ft.Text("Número adicionado"),
                    content=ft.Text("Acesse a seção 'Clientes' para visualizar o número do cliente."),
                    on_dismiss=self.cadastrar_numero,
                    bgcolor=self.tela.cor_dialogo
                ))
            else:
                self.tela.page.open(ft.AlertDialog(
                    title=ft.Text("Erro"),
                    content=ft.Text("Defina os dados do número antes de criar."),
                    bgcolor=self.tela.cor_dialogo
                ))
            self.tela.page.update()

        # Página final
        self.tela.atualizar_pagina(
            ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ADD_IC_CALL),
                    ft.Text("Adicionar número ao sistema", size=22, weight=ft.FontWeight.BOLD)
                ]),
                ft.Divider(thickness=2),
                ft.Row([configDados, info]),
                self.tela.criar_botao('Criar número', funcao=criar)
            ])
        )

        atualizar_info()  # Primeira atualização do card
