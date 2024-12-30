class Veiculo:
    def __init__(self, tipo, custo, combustivel_disponivel):
        self.tipo = tipo
        self.custo = custo
        self.combustivel_disponivel = combustivel_disponivel

    def get_custo(self):
        return self.custo

    def get_tipo(self):
        return self.tipo

    def get_combustivel_disponivel(self):
        return self.combustivel_disponivel


        #self.velocidade = velocidade
        #self.volume_carga = volume_carga # que pode transportar
