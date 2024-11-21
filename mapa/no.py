# Classe No para definição dos nós dos grafos.
# Cada nó tem um nome e um id, podendo conter outros atributos no futuro.

class No:
    # Construtor do nó, inicializa o nome e id.
    def __init__(self, name, id=-1):
        self.m_id = id
        self.m_name = str(name)
        # boolean flag que classifica como nó com recursos infinitos, 0 - seguro, 1 - necessita de ajuda
        # int num_pessoas_necessitadas
        # int tempo_critico

    # Retorna a representação em string do nó.
    def __str__(self):
        return "no " + self.m_name

    # Retorna a representação para fins de debugging.
    def __repr__(self):
        return "no " + self.m_name

    # Define o id do nó.
    def setId(self, id):
        self.m_id = id

    # Retorna o id do nó.
    def getId(self):
        return self.m_id

    # Retorna o nome do nó.
    def getName(self):
        return self.m_name

    # Compara dois nós pelo nome.
    def __eq__(self, other):
        return self.m_name == other.m_name

    # Garante que o nó pode ser usado em coleções como conjuntos e dicionários.
    def __hash__(self):
        return hash(self.m_name)
