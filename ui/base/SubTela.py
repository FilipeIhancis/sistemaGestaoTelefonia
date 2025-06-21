from ui.base.TelaBase import TelaBase
from typing import Type

class SubTela():

    def __init__(self, tela : TelaBase):
        self._tela = tela

    @property
    def tela(self):
        return self._tela
    
    @tela.setter
    def tela(self, tela):
        if not isinstance(tela, TelaBase):
            raise ValueError("Erro: tela admin não é do tipo TelaUsuario")
        self._tela = tela