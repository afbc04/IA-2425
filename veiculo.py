class Veiculo:
    def __init__(self, tipo, custo, combustivel_disponivel, limite_carga, velocidade):
        self.tipo = tipo
        self.custo = custo
        self.combustivel_disponivel = combustivel_disponivel
        self.limite_carga = limite_carga
        self.velocidade = velocidade

    def get_custo(self):
        return self.custo

    def get_tipo(self):
        return self.tipo

    def get_combustivel_disponivel(self):
        return self.combustivel_disponivel

    def get_limite_carga(self):
        return self.limite_carga

    def get_velocidade(self):
        return self.velocidade
