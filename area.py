class Area:
    def __init__(self, id = -1, pop = 0, gravidade = 1, janelaCritica= -1, caminhos = []):
        self.id = id
        self.pop = pop
        self.gravidade = gravidade
        self.janelaCritica = janelaCritica
        self.caminhos = caminhos

    def addCaminho(self,caminho):
        self.caminhos.append(caminho)