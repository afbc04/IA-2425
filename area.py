class Area:
    def __init__(self, id = -1, pop = 0, meteo = None,janelaCritica= -1, caminhos = []):
        self.id = id
        self.pop = pop
        self.meteo = meteo
        self.perigoMeteo = 0
        self.janelaCritica = janelaCritica
        self.caminhos = caminhos

    def addCaminho(self,caminho):
        self.caminhos.append(caminho)