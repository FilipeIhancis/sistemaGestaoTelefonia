from datetime import datetime

class Usuario:
    def __init__(self, nome: str, cpf: str, email: str, senha: str, data_registro: datetime):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.data_registro = data_registro

    def cpf_valido(self) -> bool:
        cpf = ''.join(filter(str.isdigit, self.cpf))

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
    

    def verifica_login(self) -> bool:
        pass
    


