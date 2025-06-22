import flet as ft
from ui.base.SubTela import SubTela
from models.solicitacao import Solicitacao

class PaginaSolicitacoes(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela_admin)


    def pagina_solicitacoes(self, solicitacoes : list[Solicitacao] = None, filtro_texto : str = 'Todas') -> None:
        
        cabecalho = ft.Row([ft.Icon(ft.Icons.CHECKLIST), ft.Text("Solicitações / Demandas", size=22, weight=ft.FontWeight.BOLD)], spacing = 5)

        # Inicialmente, exibe todas (sem filtro)
        if solicitacoes == None:
            solicitacoes = self.tela.bd.solicitacoes.obter_solicitacoes()


        def filtro_selecionado(e : ft.ControlEvent = None) -> None:
            if e.control.value == 'Pendentes':
                self.pagina_solicitacoes( self.tela.bd.solicitacoes.pendentes() , filtro_texto = 'Pendentes' )
            elif e.control.value == 'Resolvidas':
                self.pagina_solicitacoes( self.tela.bd.solicitacoes.resolvidas() , filtro_texto = 'Resolvidas' )
            else:
                self.pagina_solicitacoes()

        filtro = self.tela.dropdown(listaOpcoes=['Todas', 'Pendentes', 'Resolvidas'],
                                    tamanho=300,
                                    funcao=filtro_selecionado,
                                    texto=filtro_texto)

        self.tela.atualizar_pagina(
            ft.Column(expand = True, scroll = ft.ScrollMode.AUTO, controls = [
                cabecalho,
                ft.Divider(thickness=2),
                ft.Container(padding=ft.padding.only(top=10,bottom=25), content=
                             ft.Row([ft.Text('Filtrar solicitações', weight=ft.FontWeight.BOLD), filtro],spacing=20)
                ),
                ft.Row(wrap = True, spacing = 20, run_spacing = 20,
                    controls=[
                        self.criar_cartao_solicitacao(s) for s in solicitacoes
                    ]
                )
            ])
        )


    def criar_cartao_solicitacao(self, solicitacao : Solicitacao) -> ft.Container:

        status_text = ft.Text(color=ft.Colors.WHITE)
        if solicitacao.status:
            status_text.value = 'Resolvida'
        else:
            status_text.value = 'Pendente'

        def on_status_change(novo_status : str):
            status_text.value = novo_status
            if novo_status == 'Pendente':
                self.tela.bd.solicitacoes.tornar_pendente(solicitacao)
                self.tela.page.open(
                    ft.AlertDialog(
                        title = ft.Text(f'Solicitação {solicitacao.id} alterada'),
                        content= ft.Text("Solicitação foi alterada para status 'PENDENTE'."),
                        bgcolor = self.tela.cor_dialogo,
                        on_dismiss = lambda e : self.pagina_solicitacoes
                    )
                )
                self.tela.page.update()
            else:
                self.tela.bd.solicitacoes.tornar_resolvida(solicitacao)
                self.tela.page.open(
                    ft.AlertDialog(
                        title = ft.Text(f'Solicitação {solicitacao.id} alterada'),
                        content= ft.Text("Solicitação foi alterada para status 'RESOLVIDA'."),
                        bgcolor = self.tela.cor_dialogo,
                        on_dismiss = lambda e : self.pagina_solicitacoes
                    )
                )
                self.tela.page.update()
            
        menu = ft.PopupMenuButton(
            padding = 5, content = status_text,
            items=[ ft.PopupMenuItem(text="Pendente", on_click = lambda _: on_status_change("Pendente")),
                    ft.PopupMenuItem(text="Resolvida", on_click = lambda _: on_status_change("Resolvida"))],
            bgcolor = self.tela.cor_botao
        )

        def linha(texto1 : str = '', texto2 : str = '') -> ft.Row:
            return ft.Row(
                controls = [ft.Text(texto1, size=12, weight=ft.FontWeight.BOLD), ft.Text(texto2, size=12)],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )

        return ft.Container(
            width=300, border=ft.border.all(1), border_radius=10,
            content=ft.Column([
                # Cabeçalho sem padding lateral
                ft.Container(
                    bgcolor=self.tela.cor_cartao_2, padding=ft.padding.all(5), alignment=ft.alignment.center,
                    content=ft.Column(spacing = 10, controls=[
                        ft.Text(f"Solicitação ({solicitacao.id})", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ])
                ),
                # Corpo com padding interno
                ft.Container(
                    padding=10, content=ft.Column([
                        ft.Container(
                            border=ft.border.all(1), padding=ft.padding.all(10), border_radius=6,
                            content=ft.Column([
                                linha('Solicitante', solicitacao.cliente_solicitante.nome),
                                linha('CPF', solicitacao.cliente_solicitante.cpf)
                            ], spacing=5)
                        ),
                        ft.Container(
                            border=ft.border.all(1), padding=10, margin=ft.margin.only(bottom=5), border_radius=5,
                            content=ft.Column(spacing=5,controls=[
                                linha('Categoria', solicitacao.categoria),
                                ft.Divider(thickness=1),
                                ft.Row([ft.Text(size=12, value=f'Assunto: '), ft.Text(value=solicitacao.assunto, size = 12)]),
                                ft.Divider(thickness=1),
                                ft.Column([ft.Text('Observações: ', size=12, weight=ft.FontWeight.BOLD),
                                           ft.Text(value=solicitacao.observacoes, size=12)])
                            ])
                        ),
                        ft.Row([
                            ft.Text("Status:", weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content = menu, bgcolor = self.tela.cor_botao, padding = ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius = 10, alignment = ft.alignment.center
                            )
                        ], alignment=ft.MainAxisAlignment.END)
                    ])
                )
            ])
        )