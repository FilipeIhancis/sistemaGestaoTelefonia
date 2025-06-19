class Plano:
    def __init__(self, id_plano: int, nome_plano: str, preco: float, dados_mb: int, preco_sms: float, min_max_ligacao: int):
        self.id_plano = id_plano
        self.nome_plano = nome_plano
        self.preco = preco
        self.dados_mb = dados_mb
        self.preco_sms = preco_sms
        self.min_max_ligacao = min_max_ligacao

    def custo_minuto_excedente(self) -> float:
        # Custo do minuto extra baseado no valor médio por minuto, com acréscimo
        return (self.preco / self.min_max_ligacao) * 1.5  # Pode ajustar esse fator se quiser

    def resumo(self) -> dict:
        return {
            "nome": self.nome_plano,
            "preço": self.preco,
            "dados (MB)": self.dados_mb,
            "preço SMS": self.preco_sms,
            "minutos incluídos": self.min_max_ligacao
        }
