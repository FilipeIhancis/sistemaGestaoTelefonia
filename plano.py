class Plano:
    def __init__(self, nome_plano: str, preco: float, dados_mb: int, preco_sms: float, min_max_ligacao: int):
        self.nome_plano = nome_plano
        self.preco = preco
        self.dados_mb = dados_mb
        self.preco_sms = preco_sms
        self.min_max_ligacao = min_max_ligacao
    