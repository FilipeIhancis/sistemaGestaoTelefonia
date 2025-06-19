from interface_grafica.base.TelaUsuario import TelaUsuario

class SubTela():

    def __init__(self, tela_admin : TelaUsuario):
        self._tela = tela_admin

    @property
    def tela(self):
        return self._tela
    
    @tela.setter
    def tela(self, tela_admin):
        if not isinstance(tela_admin, TelaUsuario):
            raise ValueError("Erro: tela admin não é do tipo TelaUsuario")
        self._tela = tela_admin