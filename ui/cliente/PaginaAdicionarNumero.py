import flet as ft
from ui.base.SubTela import SubTela
from models.solicitacao import Solicitacao
from models.plano import Plano


class PaginaAdicionarNumero(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)


    def pagina_adicionar_numero(self) -> None:

        nome_plano = ''
        valor_recarga = 0
        planos_container = []
        botao_solicitar = self.tela.criar_botao('Solicitar Número')

        cabecalho = ft.Text("Adicionar novo número", size=22, weight=ft.FontWeight.BOLD)


        # Radio group de recarga
        recarga_group = ft.RadioGroup(
            content = ft.Row([
                ft.Radio(value="10", label="R$ 10,00"), ft.Radio(value="20", label="R$ 20,00"),
                ft.Radio(value="30", label="R$ 30,00"), ft.Radio(value="40", label="R$ 40,00"),])
        )

        recarga_group.value = 0

        def selecionar_plano(e : ft.ControlEvent = None) -> None:

            for plano in planos_container:
                plano.border = ft.border.all(1)
            
            # Botão selecionado recebe destaque amarelo
            e.control.border = ft.border.all(2, ft.Colors.YELLOW_300)
            e.control.bgcolor = ft.Colors.with_opacity(0.1, self.tela.cor_cartao_1)

            nonlocal nome_plano
            nome_plano = e.control.data     # nome do plano que deve adicionar
            self.tela.page.update()

        def salvar_solicitacao(e : ft.ControlEvent = None) -> None:

            self.tela.bd.solicitacoes.salvar(
                Solicitacao(
                    categoria='Solicitação', assunto='Solicitação de novo número',
                    observacoes=f'Plano: {nome_plano} - Recarga inicial: R$ {valor_recarga}',
                    cliente_solicitante=self.tela.usuario
                )
            )
            
            self.tela.page.open(
                ft.AlertDialog(
                    title=ft.Text("Número solicitado"),
                    content=ft.Text(f"Número de plano '{nome_plano}' solicitado com sucesso. Um administrador irá criar o número para você."),
                    on_dismiss = lambda e: self.pagina_adicionar_numero(),
                    bgcolor=self.tela.cor_dialogo
                )
            )
            self.tela.page.update()

        def solicitar_numero(e : ft.ControlEvent = None) -> None:
            
            valor_recarga = float(recarga_group.value)

            if nome_plano == '' or valor_recarga == 0:
                self.tela.page.open(
                    ft.AlertDialog(
                        title=ft.Text("Erro"),
                        content=ft.Text("Selecione o plano e a recarga inicial para solicitar um novo número."),
                        bgcolor=self.tela.cor_dialogo
                    )
                )
            else:
                self.tela.confirmar_identidade(titulo='Confirme sua senha', ao_confirmar = salvar_solicitacao)
                

        # OBTÉM OS PLANOS VIA BANCO DE DADOS
        planos = self.tela.bd.planos.obter_planos()
        for plano in planos:
            plano_card = self.criar_cartao_plano(plano)
            plano_card.on_click = selecionar_plano
            planos_container.append(plano_card)

        botao_solicitar.on_click = solicitar_numero

        self.tela.atualizar_pagina(
            ft.Column([
                cabecalho,
                ft.Divider(thickness=2),
                ft.Container( content=ft.Column([
                    ft.Text("Escolha seu plano", size=18, weight=ft.FontWeight.BOLD),
                    ft.Column([ft.Row([plan for plan in planos_container], alignment=ft.MainAxisAlignment.START, wrap=True)]),
                    ]),
                    padding=20, border=ft.border.all(1), border_radius=10, margin=10
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Recarga inicial", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([ ft.Text("Valor: "), recarga_group ])
                    ]),
                    padding=20, border=ft.border.all(1), border_radius=10, margin=10
                ),
                botao_solicitar
            ],
            scroll=ft.ScrollMode.AUTO
            )
        )

    def criar_cartao_plano(self, plano : Plano) -> ft.Container:

        def linha(texto1:str, texto2:str) -> ft.Row:
            return ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text(str(texto1), weight=ft.FontWeight.BOLD), ft.Text(str(texto2))])
        
        return ft.Container (
            border = ft.border.all(1), border_radius = 10, width=315, padding = 8, tooltip="Clique para selecionar", data = plano.nome,
            content = ft.Column(
                [ft.Container(padding = 10, bgcolor=self.tela.cor_cartao_2, width=float('inf'),
                              content=ft.Row([ft.Text(plano.nome, weight=ft.FontWeight.BOLD, size=17)], alignment=ft.MainAxisAlignment.CENTER)),
                ft.Container(padding = ft.padding.only(left=20,right=20,bottom=20,top=5), content=
                            ft.Column([
                                linha('Dados de Internet', str(plano.dados_mb)+' MB'),
                                linha('Máximo de ligações', str(plano.maximo_ligacao)),
                                linha('Minutos máx. de ligação', str(plano.minutos_max_ligacao)),
                                linha('Preço min. ligação extra (un.)', str(plano.pacote_minutos_unitario)),
                                linha('Máximo de mensagens', str(plano.maximo_mensagens)),
                                linha('Preço mensagens extra (un.)', str(plano.pacote_mensagem_unitario)),
                                linha('Valor Mensal', 'R$ ' + str(plano.preco))
                            ],
                            spacing = 10)
                )]
            )
        )