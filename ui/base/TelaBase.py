import flet as ft
from database.GerenciadorBanco import GerenciadorBanco
import re

class TelaBase():

    def __init__(self, page : ft.Page):
        
        self.__app = ft.app
        self._page = page
        self.__conteudo_pagina = ft.Container(expand=True, alignment=ft.alignment.center)
        self.__cor_barra_progresso : str = ''
        self.__cor_botao : str = ''
        self.__cor_cartao_1 : str = ''
        self.__cor_cartao_2 : str = ''
        self.__cor_cartao_3 : str = ''
        self.__cor_dialogo : str = ''
        self.definir_cor_azul()

        self.bd = GerenciadorBanco('database/exemplo.db')


    @property
    def app(self):
        return self.__app
    
    @app.setter
    def app(self, aplicativo):
        if not callable(aplicativo):
            raise ValueError("Aplicativo inválido: deve ser uma função")
        self.__app = aplicativo

    @property
    def login_callback(self):
        return self._login_callback
    
    @login_callback.setter
    def login_callback(self, login):
        if not callable(login):
            raise ValueError("Tela de Login inválida: precisa ser função")
        self._login_callback = login

    @property
    def page(self):
        return self._page
    
    @page.setter
    def page(self, pagina : ft.Page):
        self._page = pagina

    @property
    def conteudo_pagina(self):
        return self.__conteudo_pagina
    
    @conteudo_pagina.setter
    def conteudo_pagina(self, conteudo):
        if not isinstance(conteudo, ft.Container):
            raise ValueError("Não é do tipo Container")
        self.__conteudo_pagina = conteudo

    @property
    def cor_botao(self):
        return self.__cor_botao
    
    @cor_botao.setter
    def cor_botao(self, cor : str):
        if not self.validar_cor(cor):
            raise ValueError
        self.__cor_botao = cor
    
    @property
    def cor_cartao_1(self):
        return self.__cor_cartao_1
    
    @cor_cartao_1.setter
    def cor_cartao_1(self, cor : str):
        if not self.validar_cor(cor):
            raise ValueError
        self.__cor_cartao_1 = cor
    
    @property
    def cor_cartao_2(self):
        return self.__cor_cartao_2
    
    @cor_cartao_2.setter
    def cor_cartao_2(self, cor : str):
        if not self.validar_cor(cor):
            raise ValueError
        self.__cor_cartao_2 = cor
    
    @property
    def cor_cartao_3(self):
        return self.__cor_cartao_3
    
    @cor_cartao_3.setter
    def cor_cartao_3(self, cor : str):
        if not self.validar_cor(cor):
            raise ValueError
        self.__cor_cartao_3 = cor
    
    @property
    def cor_barra_progresso(self):
        return self.__cor_barra_progresso
    
    @cor_barra_progresso.setter
    def cor_barra_progresso(self, cor : str):
        if not self.validar_cor(cor):
            raise ValueError
        self.__cor_barra_progresso = cor

    @property
    def cor_dialogo(self):
        return self.__cor_dialogo
    
    @cor_dialogo.setter
    def cor_dialogo(self, cor):
        if not self.validar_cor(cor):
            raise ValueError
        self.__cor_dialogo = cor

    def validar_cor(self, cor : str = '') -> bool :
        if not isinstance(cor, str):
            return False
        return bool(re.match(r'^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', cor))

    def validar_email(self, e = None) -> bool :
        return True
    
    def validar_senha(self, e = None) -> bool:
        return False
    
    def validar_cpf(self, e = None) -> bool:
        return True

    
    def iniciar(self, pagina_inicio : None):
        if not callable(pagina_inicio):
            raise ValueError("Página inválida para dar início à interface gráfica")
        self.app(target = pagina_inicio)


    def atualizar_pagina(self, conteudo : ft.Column):
        self.conteudo_pagina.content = conteudo
        self.conteudo_pagina.content.scroll = ft.ScrollMode.AUTO
        self.conteudo_pagina.padding = 10
        self.conteudo_pagina.alignment = ft.alignment.top_left
        self.conteudo_pagina.update()


    def formatarNumero(self, numero : str) -> str:
        ddd = numero[:2]
        parte1 = numero[2:7]
        parte2 = numero[7:]
        return f"({ddd}) {parte1}-{parte2}"


    def criar_botao(self, texto:str='', icone : ft.Icon=None, funcao=None, cor:bool = True) -> ft.ElevatedButton:
        if cor:
            cor_botao = self.cor_botao
            return(
                ft.ElevatedButton(text = texto, bgcolor = cor_botao, color = ft.Colors.WHITE, on_click= funcao, icon = icone,
                style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius=4))))
        else:
            cor_botao = None
            return (ft.ElevatedButton(text = texto, bgcolor = cor_botao, color = ft.Colors.WHITE, on_click= funcao, icon = icone,
                style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius=4), side=ft.BorderSide(1))))
        

    def textField(self, tamanho : int = 100, prefixo : str = None, inteiro:bool = False, flutuante:bool = False, texto:bool=False, altura : int = 35) -> ft.TextField:

        def validar_input(e: ft.ControlEvent = None) -> None:

            # Obtém informações do textfield
            valor = e.control.value or ""
            novo_texto = valor

            # Verifica qual é o tipo de entrada do textfield
            if inteiro:
                novo_texto = ''.join(c for c in valor if c.isdigit())
            elif flutuante:
                novo_texto = ""
                ponto_encontrado = False
                for c in valor:
                    if c.isdigit():
                        novo_texto += c
                    elif c == "." and not ponto_encontrado:
                        novo_texto += c
                        ponto_encontrado = True
                    # ignora tudo que não for dígito ou o primeiro ponto
            elif texto:
                # Texto livre, não filtra nada
                return
            # Se o valor foi alterado, atualiza o campo
            if novo_texto != valor:
                e.control.value = novo_texto
                e.control.update()

        return ft.TextField(
            width=tamanho,
            prefix_text=prefixo,
            text_size=12,
            on_change=validar_input if (inteiro or flutuante) else None,
            border_color=ft.Colors.WHITE,
            focused_border_color=ft.Colors.WHITE,
            height=altura,
            text_align=ft.TextAlign.LEFT,
            content_padding=ft.padding.symmetric(horizontal=8, vertical=8)
        )
    

    def dropdown(self, texto : str = '', listaOpcoes : list = [], tamanho : int = 250, funcao = None) -> ft.Dropdown:
        return ft.Dropdown(
            border_width=1,
            border_color=ft.Colors.GREY,
            text_size=12,
            content_padding=ft.padding.symmetric(horizontal=8, vertical=3),
            options = [ft.dropdown.Option(elemento) for elemento in listaOpcoes],
            hint_text=texto,
            width=tamanho,
            on_change=funcao
        )


    ## IMPLEMENTAR AS CORES DEPOIS !

    def definir_cor_vermelho(self) -> None:
        self.cor_botao = "#6D2D2D"
        self.cor_cartao_1 = "#282727"
        self.cor_cartao_2 = "#442222"

    def definir_cor_azul(self) -> None:
        self.cor_botao = "#372D6D"
        self.cor_cartao_1 = "#1D1420"
        self.cor_cartao_2 = "#272244"
        self.cor_dialogo = "#1A1929"