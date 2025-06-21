from interface_grafica.base.TelaUsuario import TelaUsuario

class SubTela():

    def __init__(self, tela : TelaUsuario):
        self._tela = tela

    @property
    def tela(self):
        return self._tela
    
    @tela.setter
    def tela(self, tela):
        if not isinstance(tela, TelaUsuario):
            raise ValueError("Erro: tela admin não é do tipo TelaUsuario")
        self._tela = tela