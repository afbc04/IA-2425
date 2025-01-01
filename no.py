from meteorologia import Meteorologia

class No:
    def __init__(self, name, populacao=0, janela_tempo=24, meteorologia=None, x=0, y=0, veiculos=None, medicamento=0):
        self.m_name = str(name)
        self.x = x
        self.y = y
        self.populacao = populacao        
        self.janela_tempo = janela_tempo  
        self.meteorologia = meteorologia if meteorologia else Meteorologia()
        self.veiculos = veiculos if veiculos else []
        self.medicamento = medicamento

    def __str__(self):
        return f"no {self.m_name}"

    def __repr__(self):
        return f"no {self.m_name}"

    def getName(self):
        return self.m_name
    
    def get_coordenadas(self):
        return self.x, self.y

    def get_veiculos(self):
        return getattr(self, "veiculos", [])

    def get_medicamento(self):
        return self.medicamento  

    def set_medicamento(self, quantidade):
        self.medicamento = quantidade 

    def calcula_impacto_meteorologia(self):
        """
        Calcula o impacto das condições meteorológicas.
        Quanto maiores os valores, maior o impacto.
        """
        return (
            self.meteorologia.chuva +
            self.meteorologia.tempestade +
            self.meteorologia.vento +
            self.meteorologia.nevoeiro
        )

    def calcula_prioridade(self):
        """
        Calcula a prioridade da zona com base na população, na janela de tempo restante e no impacto meteorológico.
        Quanto menor o valor, maior a prioridade. Se for 0, é a mais prioritária.
        """
        if self.populacao == 0:
            return float('inf') 

        if self.janela_tempo == 0:
            return float('inf') 

        impacto_meteorologico = self.calcula_impacto_meteorologia()

        # Prioridade calculada: Menor valor significa maior prioridade
        return ((self.janela_tempo) / (self.populacao + impacto_meteorologico))

    def __eq__(self, other):
        return self.m_name == other.m_name

    def __hash__(self):
        return hash(self.m_name)
