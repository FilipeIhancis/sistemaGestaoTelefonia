from database.BancoDeDados import BancoDeDados, T
from models import *
from datetime import datetime

class BancoUsuario(BancoDeDados[Usuario]):

    def __init__(self, diretorio : str = ''):
        super().__init__(diretorio)


    def salvar(self, usuario : Usuario):

        if self.cpf_existe(usuario.cpf):
            print("Usuário já está cadastrado no banco de dados")
            return

        self.executar(
            """
                INSERT INTO USUARIO (nome, cpf, email, senha, tipo)
                VALUES (?, ?, ?, ?, ?)
            """,
            (usuario.nome, usuario.cpf, usuario.email, usuario.senha, usuario.tipo)
        )

    def mod(self):

        self.executar("""
        ALTER TABLE SOLICITACOES ADD COLUMN observacoes;
        """)


    def cpf_existe(self, cpf : str) -> bool:
        resultado = self.executar_select(
            """
                SELECT 1 FROM USUARIO WHERE cpf = ?
            """,
            (cpf,)
        )
        return resultado is not None and len(resultado) > 0
    
    
    def email_existe(self, email : str) -> bool:
        resultado = self.executar_select(
            """
                SELECT 1 FROM USUARIO WHERE email = ?
            """,
            (email,)
        )
        return resultado is not None and len(resultado) > 0

    
    def login(self, email : str, senha : str) -> bool:
        
        resultado = self.executar_select(
            """
                SELECT senha FROM USUARIO WHERE email = ?
            """,
            (email,)
        )

        if resultado and resultado[0][0] == senha:
            return True
        else:
            return False
        
    
    def buscar_usuario(self, email : str, senha : str) -> Usuario:
        resultado = self.executar_select(
            """
            SELECT nome, cpf, email, senha, tipo FROM USUARIO
            WHERE email = ? AND senha = ?
            """,
            (email, senha)
        )
        if resultado and len(resultado) > 0:
            linha = resultado[0]
            nome = linha[0]
            cpf = linha[1]
            tipo = linha[4]

            return Usuario(nome=nome, cpf=cpf, email=email, senha=senha, tipo=tipo, data_registro=datetime.now())
        else:
            return None
        
    
    def buscar_usuario_cpf(self, cpf : str) -> Usuario:

        resultado = self.executar_select(
            """
            SELECT nome, cpf, email, senha, tipo FROM USUARIO
            WHERE cpf = ?
            """,
            (cpf,)
        )

        if resultado and len(resultado) > 0:
            linha = resultado[0]
            nome = linha[0]
            email = linha[2]
            senha = linha[3]
            tipo = linha[4]
            return Usuario(
                nome=nome, cpf=cpf, email=email, senha=senha,
                tipo=tipo, data_registro=datetime.now()
            )
        else:
            return None
        

    def alterar_usuario(self, cpf_usuario : str = '', novo_email : str = '', nova_senha : str = '') -> None:

        campos = []
        parametros = []

        if novo_email != '':
            campos.append("email = ?")
            parametros.append(novo_email)

        if nova_senha != '':
            campos.append("senha = ?")
            parametros.append(nova_senha)

        if not campos:  # segurança
            return

        parametros.append(cpf_usuario)

        self.executar(
            f"""
            UPDATE USUARIO
            SET {', '.join(campos)}
            WHERE cpf = ?
            """,
            tuple(parametros)
        )


    def cpf_existe_email(self, cpf : str, email : str) -> bool:
        
        resultado = self.executar_select(
            """
            SELECT 1 FROM USUARIO WHERE cpf = ? AND email = ?
            """,
            (cpf, email)
        )
        return bool(resultado and len(resultado) > 0)
    

    def obter_usuarios(self) -> list[Usuario]:

        usuarios: list[Usuario] = []

        linhas = self.executar_select("""
            SELECT nome, cpf, email, senha, tipo
            FROM USUARIO
        """)

        for linha in linhas:
            nome, cpf, email, senha, tipo = linha
            usuario = Usuario(
                nome=nome,
                cpf=cpf,
                email=email,
                senha=senha,
                data_registro=datetime.now(),
                tipo=tipo
            )
            usuarios.append(usuario)

        return usuarios
    

    def obter_clientes(self) -> list[Cliente]:
        
        clientes: list[Cliente] = []

        linhas = self.executar_select("""
            SELECT nome, cpf, email, senha
            FROM USUARIO
            WHERE tipo = 'CLIENTE'
        """)

        for linha in linhas:
            nome, cpf, email, senha = linha

            # Busca os números que pertencem a este cliente
            numeros_cliente: list[Numero] = []
            linhas_numeros = self.executar_select("""
                SELECT numero, saldo
                FROM NUMEROS_TELEFONE
                WHERE cpf_cliente = ?
            """, (cpf,))

            for num_linha in linhas_numeros:
                numero = Numero(
                    numero=num_linha[0],
                    cpf_proprieatario=cpf,
                    saldo=num_linha[1],
                    assinatura=None,
                    mensagens=[],
                    ligacoes=[]
                )
                numeros_cliente.append(numero)

            cliente = Cliente(
                nome=nome,
                cpf=cpf,
                email=email,
                senha=senha,
                data_registro=datetime.now(),  # Substitua caso tenha o campo correto
                numeros=numeros_cliente
            )

            clientes.append(cliente)

        return clientes
    

    def adicionar_cliente(self, usuario : Usuario) -> bool:

        if self.cpf_existe(usuario.cpf):
            return False  # Já existe um usuário com esse CPF

        try:
            self.executar(
                """
                INSERT INTO USUARIO (nome, cpf, email, senha, tipo)
                VALUES (?, ?, ?, ?, ?)
                """,
                (usuario.nome, usuario.cpf, usuario.email, usuario.senha, 'CLIENTE')
            )
            return True
        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")
            return False
        

    def modificar_senha(self, cpf: str, nova_senha : str) -> None:
       self.executar(
            """
            UPDATE USUARIO
            SET senha = ?
            WHERE cpf = ?
            """,
            (
                nova_senha,
                cpf
            )
        )

    def modificar_email(self, cpf : str, novo_email : str) -> None:
        self.executar(
            """
            UPDATE USUARIO
            SET email = ?
            WHERE cpf = ?
            """,
            (
                novo_email,
                cpf
            )
        )