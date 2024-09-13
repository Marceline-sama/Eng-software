class Jogo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Jogo, cls).__new__(cls)
            # Inicializando o estado do jogo
            cls._instance.jogadores = []
            cls._instance.cores_disponiveis = ["vermelho", "azul", "verde", "amarelo", "preto"]
            cls._instance.territorios = ["territorio1", "territorio2", "territorio3", "territorio4", "territorio5"]
            cls._instance.baralho_de_cartas = ["carta1", "carta2", "carta3", "carta4"]
            cls._instance.objetivos = [
                "Conquistar 24 territórios", 
                "Eliminar o jogador vermelho", 
                "Conquistar 18 territórios com 2 exércitos em cada"
            ]
            cls._instance.dados_jogadores = {}
        return cls._instance
