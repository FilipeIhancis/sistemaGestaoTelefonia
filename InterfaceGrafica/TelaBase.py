import flet as ft
from abc import ABC, abstractmethod
import threading


class TelaBase(ABC):

    def __init__(self, page : ft.Page, login_callback):
        self._page = page
        self._login_callback = login_callback
        self._conteudo_pagina_principal = ft.Container(expand=True, alignment=ft.alignment.center)
        self._cor_barra_progresso : str = ''
        self._cor_botao : str = ''
        self._cor_cartao_1 : str = ''
        self._cor_cartao_2 : str = ''
        self._cor_cartao_3 : str = ''
        self.definir_cor_azul()

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

    @property
    def conteudo_pagina_principal(self):
        return self._conteudo_pagina_principal
    
    @conteudo_pagina_principal.setter
    def conteudo_pagina_principal(self, conteudo):
        if not isinstance(conteudo, ft.Container):
            raise ValueError("Não é do tipo Container")
        self._conteudo_pagina_principal = conteudo

    @property
    def cor_botao(self):
        return self._cor_botao
    
    @cor_botao.setter
    def cor_botao(self, cor : str):
        if not isinstance(cor, str):
            raise Value("Cor inválida")
        self._cor_botao = cor
    
    @property
    def cor_cartao_1(self):
        return self._cor_cartao_1
    
    @cor_cartao_1.setter
    def cor_cartao_1(self, cor : str):
        if not isinstance(cor, str):
            raise ValueError("Cor inválida")
        self._cor_cartao_1 = cor
    
    @property
    def cor_cartao_2(self):
        return self._cor_cartao_2
    
    @cor_cartao_2.setter
    def cor_cartao_2(self, cor : str):
        if not isinstance(cor, str):
            raise ValueError("Cor inválida")
        self._cor_cartao_2 = cor
    
    @property
    def cor_cartao_3(self):
        return self._cor_cartao_3
    
    @cor_cartao_3.setter
    def cor_cartao_3(self, cor : str):
        if not isinstance(cor, str):
            raise ValueError("Cor inválida")
        self._cor_cartao_3 = cor
    
    @property
    def cor_barra_progresso(self):
        return self._cor_barra_progresso
    
    @cor_barra_progresso.setter
    def cor_barra_progresso(self, cor : str):
        if not isinstance(cor, str):
            raise ValueError("Cor inválida")
        self._cor_barra_progresso = cor
    
    @abstractmethod
    def pagina_principal(self) -> None:
        pass

    @abstractmethod
    def paginas_menu_lateral(self, e : ft.ControlEvent) -> None:
        pass

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
        

    def textField(self, tamanho : int = 100, prefixo : str = None, inteiro:bool = False, flutuante:bool = False, altura : int = 35) -> ft.TextField:

        def validar_input(e):

            texto = e.control.value
            novo_texto = ""

            if inteiro:
                # Permite apenas dígitos (1 a 9...) e não permite zero como primeiro dígito
                novo_texto = ''.join([c for c in texto if c.isdigit()])
                # Remove zeros à esquerda
                if novo_texto.startswith("0"):
                    novo_texto = novo_texto.lstrip("0")
                # Se for vazio depois da limpeza, zera
                if novo_texto == "":
                    novo_texto = ""
            elif flutuante:
                ponto_encontrado = False
                for i, c in enumerate(texto):
                    if c.isdigit():
                        novo_texto += c
                    elif c == "." and not ponto_encontrado and i != 0:
                        novo_texto += c
                        ponto_encontrado = True

            # Atualiza o campo só se o texto tiver sido modificado
            if texto != novo_texto:
                e.control.value = novo_texto
                self.page.update()

        return ft.TextField(width=tamanho, prefix_text=prefixo, text_size = 12, on_change=validar_input,
                            border_color=ft.Colors.WHITE, focused_border_color=ft.Colors.WHITE, height = altura,
                            text_align=ft.TextAlign.LEFT, content_padding=ft.padding.symmetric(horizontal=8, vertical=8))


    def definir_cor_vermelho(self) -> None:
        self.cor_botao = "#372D6D"
        self.cor_cartao_1 = "#282727"
        self.cor_cartao_2 = "#272244"


    def definir_cor_azul(self) -> None:
        self.cor_botao = "#372D6D"
        self.cor_cartao_1 = "#1D1420"
        self.cor_cartao_2 = "#272244"