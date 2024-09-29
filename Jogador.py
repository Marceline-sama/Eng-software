class Jogador:
    def __init__(self, nome, cor):
        self.nome = nome
        self.cor = cor
        self.territorios = []
        self.cartas = []
        self.objetivo = None
        self.exercitos = 0

    def __repr__(self):
        return f"Jogador {self.nome} (Cor: {self.cor})"
