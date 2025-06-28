import flet as ft
from ui.base.SubTela import SubTela
from models.cliente import Cliente
from models.numero import Numero
from models.usuario import Usuario
from models.plano import Plano
from models.assinatura import Assinatura
from datetime import datetime


class PaginaClientes(SubTela):

    def __init__(self, tela_admin):
        super().__init__(tela=tela_admin)
        

    def criar_cartao_cliente(self, cliente : Cliente) -> ft.Container:

        num_cliente_container = ft.Container(bgcolor = self.tela.cor_cartao_1, border_radius = 10, padding = 10)
        if cliente.numeros == [] or cliente.numeros == None:
            num_cliente_container.content = ft.Text("Não possui números")
        else:
            num_cliente_container.content = ft.Column(
                [ft.Text("Números", weight=ft.FontWeight.BOLD),
                    *[
                        ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                                ft.Text(self.tela.formatarNumero(numero.numero), expand=True),
                                self.tela.criar_botao('Editar', cor = False,
                                                        funcao = lambda e, num=numero : self.pagina_edicao_numero(cliente=cliente, numero=num))
                        ])
                        for numero in cliente.numeros
                    ]
                ])

        return ft.Container(
            bgcolor = self.tela.cor_cartao_3, alignment= ft.alignment.top_left, border_radius = 5, padding = 10, border=ft.border.all(1), width=280,
            content=ft.Column([
                # Topo com ícone e email
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Row([ft.Icon(ft.Icons.PERSON, size=30), ft.Text(cliente.email, weight=ft.FontWeight.BOLD)]),
                    ft.IconButton(icon = ft.Icons.SETTINGS, on_click = lambda e : self.editar_dados_cliente(cliente=cliente))
                ]),
                ft.Divider(),
                # Área de números com botão editar
                num_cliente_container,
                ft.Container( alignment=ft.alignment.center,  padding=10,
                    content= ft.Row([self.tela.criar_botao('Ver faturas', funcao=self.tela.faturas.ver_faturas_cliente),
                                    self.tela.criar_botao('Adicionar número', funcao=self.tela.cadastros.cadastrar_numero)],
                                    spacing = 10, alignment=ft.alignment.center)
                )],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
    

    def pagina_clientes(self) -> None:

        # Obtém lista de objetos do tipo Cliente
        clientes = self.tela.bd.usuarios.obter_clientes()

        cabecalho = ft.Container(content=ft.Column([
            ft.Row(  [ ft.Row([ft.Icon(ft.Icons.PHONE),ft.Text("Clientes cadastrados", size = 22, weight = ft.FontWeight.BOLD)]),
                       ft.Row([self.tela.criar_botao("Cadastrar cliente", icone=ft.Icons.ADD, funcao=self.tela.cadastros.cadastrar_cliente)])], spacing = 15, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]))

        self.tela.atualizar_pagina(
            ft.Column( scroll = ft.ScrollMode.AUTO, controls = 
                [cabecalho,
                ft.Divider(thickness=2),
                ft.Row( 
                    wrap=True, spacing=20, run_spacing=20, expand = True, scroll = ft.ScrollMode.AUTO,
                    controls=[ self.criar_cartao_cliente(c) for c in clientes]
                )
                ])
        )


    def pagina_edicao_numero(self, e : ft.ControlEvent = None, cliente : Cliente = None, numero : Numero = None) -> None:
        
        numero = self.tela.bd.numeros.obter_numero(numero.numero)
        numero.assinatura = self.tela.bd.assinaturas.obter_assinatura(numero.numero)
        cpfs = [usuario_cliente.cpf for usuario_cliente in self.tela.bd.usuarios.obter_clientes()]
        cpfs.remove(cliente.cpf)
        planos = [plano.nome for plano in self.tela.bd.planos.obter_planos()]
        nome_cliente = cliente.nome

        cabecalho = ft.Container(content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.PHONE),ft.Text(f"Edição de Número: {self.tela.formatarNumero(numero.numero)}", size = 22, weight = ft.FontWeight.BOLD)], spacing = 15),
            ft.Row([ft.Icon(ft.Icons.ACCOUNT_CIRCLE), ft.Text(f"Cliente: {nome_cliente} - CPF: {cliente.cpf}", size = 14)], spacing=15)
        ]))

        def modificar_num( e : ft.ControlEvent = None ) -> None:
            nonlocal numero
            nonlocal novo_plano
            nonlocal novo_proprieatario
            if novo_proprieatario.value:
                self.modificar_proprieatario(numero=numero, novo_proprieatario=novo_proprieatario.value)
            if novo_plano.value:
                self.modificar_plano(numero=numero, novo_plano=novo_plano.value)

        salvar = self.tela.criar_botao("Salvar", funcao = modificar_num)
        salvar.disabled = True

        def on_change_novo_proprieatario(e = None):
            nonlocal salvar
            if novo_proprieatario.value:
                novo_proprieatario.label = ''
                novo_proprieatario.update()
                salvar.disabled = False
                self.tela.page.update()

        def on_change_novo_plano(e = None):
            nonlocal salvar
            if novo_plano.value:
                novo_plano.label=''
                novo_plano.update()
                salvar.disabled = False
                self.tela.page.update()
            
        novo_proprieatario = self.tela.dropdown(tamanho=220, listaOpcoes = cpfs)
        novo_proprieatario.on_change = on_change_novo_proprieatario
        novo_proprieatario.label = "CPF"
        novo_plano = self.tela.dropdown(tamanho=220, listaOpcoes = planos)
        novo_plano.on_change = on_change_novo_plano
        novo_plano.label = "PLANO"

        
        campo2 = ft.Container( height=250,border = ft.border.all(1), border_radius = 6, padding = 20, expand=True, bgcolor=self.tela.cor_cartao_3,
            content=ft.Column([
                ft.Row( [ft.Icon(ft.Icons.MANAGE_ACCOUNTS), ft.Text("Gerenciamento do Número", weight=ft.FontWeight.BOLD, size=16)],spacing=10),
                ft.Divider(thickness=2),
                ft.Column(controls=[    
                    ft.Row([ft.Text("Trocar Proprietário:"), novo_proprieatario], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([ft.Text("Trocar Plano:"), novo_plano], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]),
                # Linha dos dois botões no final
                ft.Row(controls=[
                        self.tela.criar_botao('Suspender número', cor=False,
                                        funcao = lambda e: self.tela.confirmar(aviso="O número será suspenso após análise.", ao_confirmar=self.suspender_numero)),
                        self.tela.criar_botao('Cancelar número', cor=False,
                                        funcao= lambda e : self.tela.confirmar_identidade(titulo='Cancelar número', ao_confirmar=self.cancelar_numero))
                    ], alignment=ft.alignment.top_left, spacing=6)
        ]))

        def linha(texto1:str='', texto2:str='') -> ft.Row:
            return ft.Row(
                controls=[ft.Text(texto1, weight=ft.FontWeight.BOLD), ft.Text(texto2)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        
        plano_nome = 'Sem plano'
        if numero.assinatura and numero.assinatura.plano:
            plano_nome = numero.assinatura.plano.nome

        status = 'Sem assinatura'
        if numero.assinatura:
            status = 'Ativa' if numero.assinatura.ativa else 'Inativa'

        campo1 = ft.Container(height=250, expand=True, border = ft.border.all(1), border_radius = 6, padding = 20, bgcolor=self.tela.cor_cartao_3,
            content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.INFO), ft.Text("Informações Gerais", weight=ft.FontWeight.BOLD, size=16)],spacing=10),
                    ft.Divider(thickness=2),
                    ft.Column(spacing = 15, controls=[
                                linha('Número', f'{self.tela.formatarNumero(numero.numero)}'),
                                linha('Proprietário', cliente.cpf),
                                linha('Plano Associado', f'{plano_nome}'),
                                linha('Status', f'{status}')
                            ])
        ]))

        self.tela.atualizar_pagina(
            ft.Column(scroll = ft.ScrollMode.AUTO, controls=[
                cabecalho, ft.Divider(thickness=2), ft.Column([ft.Row([campo1, campo2]), salvar], spacing=25)]
            )
        )


    def modificar_proprieatario(self, e : ft.ControlEvent = None, numero : Numero = None,  novo_proprieatario : str = ''):
        self.tela.bd.numeros.modificar_proprieatario(numero, novo_proprieatario)
        self.tela.page.open(self.tela.dialogo(title=ft.Text("Número alterado com sucesso"),
                                              content=ft.Text(f"Proprieatário do número {numero.numero} alterado para {novo_proprieatario}"),
                                              on_dimiss=self.pagina_clientes))
        self.tela.page.update()

    def modificar_plano(self, e : ft.ControlEvent = None, numero : Numero = None, novo_plano : str = ''):
        plano = self.tela.bd.planos.obter_plano(novo_plano)     # busca o plano através do nome
        id_ass = self.tela.bd.assinaturas.obter_id_assinatura(numero.numero)   # obtém a assinatura associada ao número
        nova_assinatura = Assinatura(plano, datetime.now(), True)
        self.tela.bd.assinaturas.modificar(id_ass, nova_assinatura)
        self.tela.page.open(self.tela.dialogo(title=ft.Text("Número alterado com sucesso"),
                                              content=ft.Text(f"Assinatura do número {numero.numero} alterada para o plano '{novo_plano}'"),
                                              on_dimiss=self.pagina_clientes))
        self.tela.page.update()


    def suspender_numero(self, e:ft.ControlEvent = None) -> None:
        
        print("Irá suspender o número")


    def cancelar_numero(self, e:ft.ControlEvent = None) -> None:

        print("Irá cancelar o número")

    
    def editar_dados_cliente(self, e : ft.ControlEvent = None, cliente : Usuario = None) -> None:

        dialogo = None
        novo_email_usuario = self.tela.textField(tamanho=130, texto=True)
        nova_senha_usuario = self.tela.textField(tamanho=130, texto=True)

        confirmar = ft.TextButton("Confirmar", disabled=True)
        mensagem_erro = ft.Text('Senha incorreta! Tente novamente.', color=ft.Colors.RED, visible=False)

        def verificar_campos(e = None):
            nonlocal confirmar
            confirmar.disabled = not (novo_email_usuario.value and nova_senha_usuario.value)
            self.tela.page.update()

        def fechar_dialogo(e=None):
            nonlocal dialogo
            self.tela.page.close(dialogo)
            self.tela.page.update()

        def confirmar_acao(e=None):
            
            nonlocal cliente
            nonlocal novo_email_usuario
            nonlocal nova_senha_usuario

            if nova_senha_usuario.value:
                if nova_senha_usuario.value == cliente.senha:
                    fechar_dialogo
                    self.tela.page.open(self.tela.dialogo(title=ft.Text("Senha permanece a mesma")))
                    self.tela.page.update()
                else:
                    self.tela.bd.usuarios.modificar_senha(cliente.cpf, nova_senha_usuario.value)
                    fechar_dialogo()
                    self.tela.page.open(self.tela.dialogo(title=ft.Text("Senha alterada com sucesso")))

            if novo_email_usuario.value:
                if novo_email_usuario.value == cliente.email:
                    fechar_dialogo
                    self.tela.page.open(self.tela.dialogo(title=ft.Text("Email permaneceu o mesmo")))
                    self.tela.page.update()
                else:
                    self.tela.bd.usuarios.modificar_email(cliente.cpf, novo_email_usuario.value)
                    fechar_dialogo()
                    self.tela.page.open(self.tela.dialogo(title=ft.Text("Email alterado com sucesso")))
                    self.tela.page.update()

        def cancelar_acao(e=None):
            fechar_dialogo()

        nova_senha_usuario.on_change = verificar_campos
        novo_email_usuario.on_change = verificar_campos

        # Define o que o botão "Solicitar" vai fazer
        confirmar.on_click = confirmar_acao

        def linha(conteudo1, conteudo2) -> ft.Row:
            return ft.Row([conteudo1, conteudo2], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Cria a caixa de diálogo padrão
        dialogo = ft.AlertDialog(
            modal=True, bgcolor=self.tela.cor_dialogo,
            title=ft.Row([ft.Icon(ft.Icons.MANAGE_ACCOUNTS), ft.Text('Editar dados do cliente', weight=ft.FontWeight.BOLD)], spacing=5),
            content=ft.Container(width=550, height=320, padding=20,
                content= ft.Column([
                    ft.Text("Deixe o campo em branco se não quiser alterar."),
                    ft.Container(padding=ft.padding.all(20), border=ft.border.all(1), border_radius=6, content=ft.Column([
                        linha(ft.Row([ft.Icon(ft.Icons.PERSON), ft.Text("Cliente (CPF)")]), ft.Text(cliente.cpf)),
                        linha(ft.Text("Email atual"), ft.Text(cliente.email)),
                        linha(ft.Text("Senha atual"), ft.Text(cliente.senha))
                    ])),
                    linha(ft.Text("Novo email do usuário", weight=ft.FontWeight.BOLD), novo_email_usuario),
                    linha(ft.Text("Nova senha do usuário", weight=ft.FontWeight.BOLD), nova_senha_usuario)
                ], spacing=15)
            ),
            actions=[confirmar, ft.TextButton("Cancelar", on_click=cancelar_acao)]
        )
        self.tela.page.dialog = dialogo
        self.tela.page.open(dialogo)
        self.tela.page.update()