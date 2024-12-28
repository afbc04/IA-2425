class No:
    def __init__(self, name, id=-1, populacao=0, janela_tempo=24, ):
        self.m_id = id
        self.m_name = str(name)
        self.populacao = populacao        # População da zona
        self.janela_tempo = janela_tempo  # Janela de tempo crítica em horas
        self.meteorologia = 

    def __str__(self):
        return f"no {self.m_name}"

    def __repr__(self):
        return f"no {self.m_name}"

    def setId(self, id):
        self.m_id = id

    def getId(self):
        return self.m_id

    def getName(self):
        return self.m_name

    def calcula_prioridade(self):
        """
        Calcula a prioridade da zona com base na população e na janela de tempo restante.
        Retorna 0 se a janela de tempo estiver esgotada, tendo a maior prioridade.
        """
        if self.janela_tempo <= 0:
            return 0  
        return self.populacao / self.janela_tempo

    def __eq__(self, other):
        return self.m_name == other.m_name

    def __hash__(self):
        return hash(self.m_name)
