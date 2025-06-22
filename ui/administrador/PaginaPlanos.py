import flet as ft
from ui.base.SubTela import SubTela
from ui.administrador.PaginaCadastros import PaginaCadastro
from models.plano import Plano

class PaginaPlanos(SubTela):


    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)
        self.cadastros = PaginaCadastro(tela_admin = tela_admin)


    def pagina_planos(self, e : ft.ControlEvent = None) -> None:

        # Obtém todos os planos do banco de dados:
        planos = self.tela.bd.planos.obter_planos()

        cabecalho = ft.Container(content=ft.Row([
            ft.Column([ft.Text("Planos", weight=ft.FontWeight.BOLD, size = 22)], alignment=ft.alignment.top_left),
            ft.Column([self.tela.criar_botao("Adicionar plano", icone=ft.Icons.ADD, funcao = self.cadastros.cadastrar_plano, cor=False)], alignment=ft.alignment.top_right)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        
        cartoes_planos = ft.Column(expand = True, controls=[
            ft.Row(wrap=True, spacing=15, run_spacing=10, controls = [
                self.criar_cartao_plano(plano, lambda e, p = plano: self.excluir_plano(plano = p)) for plano in planos
            ])]
        )
        self.tela.atualizar_pagina( ft.Column( controls=[cabecalho, ft.Divider(thickness=2), cartoes_planos], scroll=ft.ScrollMode.AUTO) )


    def criar_cartao_plano(self, plano : Plano, on_excluir : callable) -> ft.Container:

        def linha(label, valor):
            return ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=5,
                controls=[
                    ft.Text(label, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(valor, size=12),
                ]
            )
        return ft.Container(
            width=260, border=ft.border.all(1), border_radius=6, padding=8,content=
            ft.Column(spacing=10, controls=[
                # Cabeçalho
                ft.Container(
                    bgcolor=self.tela.cor_cartao_2, padding=ft.padding.all(6), alignment=ft.alignment.center,
                    content=ft.Text(plano.nome, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.BOLD),
                ),
                # Informações
                ft.Container(
                    bgcolor=self.tela.cor_cartao_1, border_radius=4, padding=ft.padding.all(8),
                    content=ft.Column([
                            linha("VALOR:", f"R$ {plano.preco}"),
                            linha("INTERNET:", f"{plano.dados_mb} GB"),
                            linha("MINUTOS MÁX. LIGAÇÃO:", str(plano.maximo_ligacao)),
                            linha("QTD. MÁX LIGAÇÕES", str(plano.maximo_ligacao)),
                            linha("QTD. MÁX MENSAGENS:", str(plano.maximo_mensagens)),
                            linha("PACOTE DE MENSAGEM UN.", str(plano.pacote_mensagem_unitario)),
                            linha("PACOTE MINUTOS DE LIGAÇÃO UN.", str(plano.pacote_minutos_unitario))
                        ], spacing=10
                    )
                ),
                # Botões
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8, controls=[
                        self.tela.criar_botao("Editar", funcao = self.editar_plano),
                        self.tela.criar_botao("Excluir", funcao = on_excluir) ]
                )
            ])
        )
    
    def editar_plano(self, e = None) -> None:

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
                self.tela.page.update()
            
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
                ft.ElevatedButton("Salvar", bgcolor=self.tela.cor_botao, color=ft.Colors.WHITE),
                ft.ElevatedButton("Cancelar", bgcolor=self.tela.cor_botao, color=ft.Colors.WHITE),
            ],
            spacing=8, alignment=ft.MainAxisAlignment.START,
        )
        # Conteúdo principal
        self.tela.atualizar_pagina(
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


    def excluir_plano(self, e : ft.ControlEvent = None, plano : Plano = None):

        if( self.tela.bd.planos.excluir_plano(plano.nome) ):
            self.tela.page.open(ft.AlertDialog(
                title=ft.Text("Plano excluído"),
                content=ft.Text("O plano '' foi excluído com sucesso. Nenhuma assinatura ativa contendo esse plano foi encontrada."),
                bgcolor=self.tela.cor_dialogo,
                on_dismiss = self.pagina_planos
            )) 
        else:
            self.tela.page.open(ft.AlertDialog(
                title=ft.Row([ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED), ft.Text("Erro")], spacing=5),
                content=ft.Text("Verifique se o algum cliente contém assinatura ativa nesse plano."),
                bgcolor=self.tela.cor_dialogo,
                on_dismiss=self.pagina_planos
            ))