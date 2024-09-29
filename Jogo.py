import threading
from random import choice, shuffle

class Jogo:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Jogo, cls).__new__(cls, *args, **kwargs)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Inicializando dados do jogo
        self.jogadores = {}
        self.territorios = []
        self.baralho_de_cartas = []
        self.objetivos = [
            "Conquistar 24 territórios", 
            "Eliminar o jogador vermelho", 
            "Conquistar 18 territórios com 2 exércitos em cada"
        ]
        self.cores_disponiveis = ["vermelho", "azul", "verde", "amarelo", "preto"]

        # Inicializar territórios e cartas
        self.inicializar_territorios()
        self.inicializar_baralho()

    @staticmethod
    def get_instance():
        return Jogo()

    # Factory Method para criar jogador
    def criar_jogador(self, nome, cor):
        if cor not in self.cores_disponiveis:
            raise ValueError(f"A cor {cor} não está disponível.")
        
        jogador = Jogador(nome, cor)
        self.jogadores[nome] = jogador
        self.cores_disponiveis.remove(cor)
        return jogador

    # Factory Method para inicializar territórios
    def inicializar_territorios(self):
        nomes_territorios = ["territorio1", "territorio2", "territorio3", "territorio4", "territorio5"]
        for nome in nomes_territorios:
            self.territorios.append(Territorio(nome))

    # Factory Method para inicializar o baralho de cartas
    def inicializar_baralho(self):
        tipos_cartas = ["carta1", "carta2", "carta3", "carta4"]
        for tipo in tipos_cartas:
            self.baralho_de_cartas.append(Carta(tipo))