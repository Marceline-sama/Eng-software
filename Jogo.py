import threading

class Jogo:
    _instance = None
    _lock = threading.Lock()  # Adicionando o lock

    def __init__(self):
        if Jogo._instance is not None:
            raise Exception("Esta classe é um singleton!")
        self.jogadores = {}
        self.cores_disponiveis = ["vermelho", "azul", "verde", "amarelo", "preto"]
        self.territorios = ["territorio1", "territorio2", "territorio3", "territorio4", "territorio5"]
        self.baralho_de_cartas = ["carta1", "carta2", "carta3", "carta4"]
        self.objetivos = ["Conquistar 24 territórios", "Eliminar o jogador vermelho", "Conquistar 18 territórios com 2 exércitos em cada"]

    @staticmethod
    def get_instance():
        with Jogo._lock:
            if Jogo._instance is None:
                Jogo._instance = Jogo()
            return Jogo._instance
