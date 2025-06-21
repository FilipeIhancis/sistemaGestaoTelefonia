from datetime import datetime

class Usuario:

    def __init__(self, nome: str, cpf: str, email: str, senha: str, data_registro: datetime, tipo : str = ''):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.data_registro = data_registro
        self.tipo = tipo.upper()

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
        return self._senha
    
    @senha.setter
    def senha(self, nova_senha : str):
        if not isinstance(nova_senha, str) or nova_senha == '' or nova_senha == ' ':
            raise ValueError
        self._senha = nova_senha

    @property
    def data_registro(self):
        return self.__data_registro
    
    @data_registro.setter
    def data_registro(self, data : datetime):
        if not isinstance(data, datetime):
            raise ValueError
        self.__data_registro = data

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, novo_email : str):
        if not isinstance(novo_email, str):
            raise ValueError
        self._email = novo_email


    def cpf_valido(self, cpf : str = '') -> bool:

        cpf = ''.join(filter(str.isdigit, cpf))

        # Confere se o CPF tem 11 dígitos e se não é uma sequência repetida
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        # Cálculo do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        # Cálculo do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        # Retorno da validação final
        return cpf[-2:] == f"{digito1}{digito2}"