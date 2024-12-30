class Veiculo:
    def __init__(self, tipo, custo):

        self.tipo = tipo # avião, carro, ...
        self.custo = custo # é mais dispendioso usar um avião do que um carro

    def get_custo(self):
        return self.custo

    def get_tipo(self):
        return self.tipo



        #self.combustivel_disponivel = combustivel_disponivel
        #self.velocidade = velocidade
        #self.volume_carga = volume_carga # que pode transportar
