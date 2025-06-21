from datetime import datetime

class Usuario:
    def __init__(self, nome: str, cpf: str, email: str, senha: str, data_registro: datetime):

        self.nome = nome
        self.__cpf = cpf
        self.__email = email
        self.__senha = senha
        self.__data_registro = data_registro

    @property
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    def cpf(self, novo_cpf : str):
        if not isinstance(novo_cpf, str) or novo_cpf == '' or not self.cpf_valido(novo_cpf):
            raise ValueError
        self.__cpf = novo_cpf

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, nova_senha : str):
        if not isinstance(nova_senha, str) or nova_senha == '' or nova_senha == ' ':
            raise ValueError
        self.__senha = nova_senha

    @property
    def data_registro(self):
        return self.__data_registro
    
    @property
    def data_registro(self, data : datetime):
        if not isinstance(data, datetime):
            raise ValueError
        self.__data_registro = data

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, novo_email : str):
        if not isinstance(novo_email, str):
            raise ValueError
        self.__email = novo_email


    def cpf_valido(self, cpf : str = '') -> bool:

        cpf = ''.join(filter(str.isdigit, cpf))

        # Confere se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return False
        if cpf == cpf[0] * 11:
            return False

        # Validação do primeiro dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10) % 11
        if digito1 == 10:
            digito1 = 0

        # Validação do segundo dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10) % 11

        if digito2 == 10:
            digito2 = 0

        return cpf[-2:] == f"{digito1}{digito2}"
    
