class Caminho:
    def __init__(self, origem = -1, destino = -1, meteo = None, veiculos = [],bloqueada = False):
        self.origem = origem
        self.destino = destino
        self.veiculosPermitidos = veiculos
        self.meteo = meteo
        self.bloqueada = bloqueada

    def addVeiculoPermitido(self,veiculo):
        self.veiculosPermitidos.append(veiculo)

