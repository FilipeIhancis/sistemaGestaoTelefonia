from .assinatura import Assinatura
from .ligacao import Ligacao
from .mensagem import Mensagem


class Numero:

    def __init__(self, numero : str = '', cpf_proprieatario : str = '', saldo : float = 0.0, assinatura : Assinatura = None,
                 mensagens : list[Mensagem] = None, ligacoes : list[Ligacao] = None):

        self.numero : str = numero
        self.cpf_proprieatario : str = cpf_proprieatario
        self.saldo = saldo
        self.assinatura = assinatura
        self.mensagens : list[Mensagem] = mensagens
        self.ligacoes : list[Ligacao] = ligacoes

    
    @property
    def numero(self):
        return self.__numero
    
    @numero.setter
    def numero(self, num : str):
        if not isinstance(num, str):
            raise ValueError
        self.__numero = num

    @property
    def cpf_proprieatario(self):
        return self.__cpf_proprieatario
    
    @cpf_proprieatario.setter
    def cpf_proprieatario(self, cpf : str):
        if not isinstance(cpf, str):
            raise ValueError
        self.__cpf_proprieatario = cpf

    @property
    def saldo(self) -> float:
        return self.__saldo

    @saldo.setter
    def saldo(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise ValueError("Saldo precisa ser numérico.")
        self.__saldo = float(valor)

    @property
    def assinatura(self) -> Assinatura:
        return self.__assinatura

    @assinatura.setter
    def assinatura(self, ass: Assinatura):
        if ass is not None and not isinstance(ass, Assinatura):
            raise ValueError("Assinatura inválida.")
        self.__assinatura = ass

    @property
    def mensagens(self) -> list[Mensagem]:
        return self.__mensagens if self.__mensagens is not None else []

    @mensagens.setter
    def mensagens(self, msgs: list[Mensagem]):
        if msgs is not None and not all(isinstance(m, Mensagem) for m in msgs):
            raise ValueError("Todos os itens devem ser objetos da classe Mensagem.")
        self.__mensagens = msgs

    @property
    def ligacoes(self) -> list[Ligacao]:
        return self.__ligacoes if self.__ligacoes is not None else []

    @ligacoes.setter
    def ligacoes(self, lgs: list[Ligacao]):
        if lgs is not None and not all(isinstance(l, Ligacao) for l in lgs):
            raise ValueError("Todos os itens devem ser objetos da classe Ligacao.")
        self.__ligacoes = lgs
        